# Shared fail-closed synchronization guard. State contains hashes only, never file contents.
function Get-SyncManifest([string]$Root) {
    $m = @{}
    Get-ChildItem -LiteralPath $Root -Recurse -File -Force | Where-Object {
        $_.FullName -notmatch '\\(node_modules|\.git|__pycache__|_backup_[^\\]*)\\' -and $_.Name -notmatch '^\.env' -and $_.Extension -ne '.key'
    } | ForEach-Object { $m[$_.FullName.Substring($Root.Length).TrimStart('\')] = (Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256).Hash }
    return $m
}
function Start-SafeSkillSync([string]$Skill, [string]$Source, [string[]]$Targets, [string]$StateRoot = (Join-Path $env:USERPROFILE '.skill-sync')) {
    $Source = [IO.Path]::GetFullPath($Source).TrimEnd('\')
    if ($Skill -notmatch '^[a-zA-Z0-9_-]+$') { throw 'Invalid skill name.' }
    New-Item -ItemType Directory -Path $StateRoot -Force | Out-Null
    $lock = [IO.File]::Open((Join-Path $StateRoot "$Skill.lock"), 'OpenOrCreate', 'ReadWrite', 'None')
    try {
        $stateFile = Join-Path $StateRoot "$Skill.json"
        $prior = @{}
        if (Test-Path -LiteralPath $stateFile) {
            $saved = Get-Content -LiteralPath $stateFile -Raw -Encoding UTF8 | ConvertFrom-Json
            if ($saved.Source -ne $Source) { throw "Canonical source is '$($saved.Source)'; refusing a different source '$Source'." }
            foreach ($p in $saved.Files.PSObject.Properties) { $prior[$p.Name] = $p.Value }
        }
        $manifest = Get-SyncManifest $Source
        if (!$manifest.ContainsKey('SKILL.md')) { throw 'Missing SKILL.md.' }
        $conflicts = [Collections.Generic.List[string]]::new()
        foreach ($target in $Targets) {
            if (!(Test-Path -LiteralPath $target)) { continue }
            foreach ($rel in $manifest.Keys) {
                $path = Join-Path $target $rel
                if (!(Test-Path -LiteralPath $path -PathType Leaf)) { continue }
                $hash = (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash
                if ($hash -ne $manifest[$rel] -and (!$prior.ContainsKey($rel) -or $hash -ne $prior[$rel])) {
                    $conflicts.Add("$path [destination=$hash; source=$($manifest[$rel])]")
                }
            }
            # Previously installed files removed locally also represent a change.
            foreach ($rel in $prior.Keys) {
                if ($manifest.ContainsKey($rel) -and !(Test-Path -LiteralPath (Join-Path $target $rel))) {
                    $conflicts.Add("$(Join-Path $target $rel) [local deletion; reconcile before restoring]")
                }
            }
        }
        if ($conflicts.Count) { throw "SYNC BLOCKED before any copy. Reconcile these files with the canonical source, then retry (no force bypass):`n$($conflicts -join "`n")" }
        return @{ Lock=$lock; Source=$Source; Targets=$Targets; Manifest=$manifest; StateFile=$stateFile }
    } catch { $lock.Dispose(); throw }
}
function Complete-SafeSkillSync($Context) {
    try {
        $current = Get-SyncManifest $Context.Source
        if ($current.Count -ne $Context.Manifest.Count) { throw 'Source changed during synchronization.' }
        foreach ($rel in $Context.Manifest.Keys) {
            if ($current[$rel] -ne $Context.Manifest[$rel]) { throw "Source changed during synchronization: $rel" }
            foreach ($target in $Context.Targets) {
                $path = Join-Path $target $rel
                if (!(Test-Path -LiteralPath $path -PathType Leaf) -or (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash -ne $current[$rel]) { throw "Incomplete synchronization: $path. Baseline not advanced." }
            }
        }
        $temp = $Context.StateFile + '.' + [guid]::NewGuid().ToString('N') + '.tmp'
        @{ Source=$Context.Source; Files=$current; VerifiedUtc=[DateTime]::UtcNow.ToString('o') } | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath $temp -Encoding UTF8
        Move-Item -LiteralPath $temp -Destination $Context.StateFile -Force
    } finally { $Context.Lock.Dispose() }
}
