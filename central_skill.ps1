function Resolve-CentralSkillPath([string]$Path) {
 $full=[IO.Path]::GetFullPath($Path).TrimEnd('\')
 for($n=0;$n -lt 12;$n++){
  $item=Get-Item -LiteralPath $full -Force
  if(!($item.Attributes -band [IO.FileAttributes]::ReparsePoint)){return $full}
  $next=@($item.Target)[0];if(!$next){throw "Unresolved link: $full"}
  $full=if([IO.Path]::IsPathRooted($next)){[IO.Path]::GetFullPath($next)}else{[IO.Path]::GetFullPath((Join-Path $item.Parent.FullName $next))}
 }
 throw 'Link cycle detected.'
}
function Get-CentralSkillTargets([string]$Skill) {
 $paths=[Collections.Generic.List[string]]::new()
 foreach($ia in @('.agents','.claude','.codex','.copilot','.gemini','.gemini\antigravity','.config\opencode','.cursor','.qwen','.codeium\windsurf')){
  if(Test-Path -LiteralPath (Join-Path $env:USERPROFILE $ia)){$paths.Add((Join-Path $env:USERPROFILE "$ia\skills\$Skill"))}
 }
 foreach($top in Get-ChildItem -LiteralPath $env:USERPROFILE -Directory -Force | Where-Object Name -ne AppData){
  foreach($dir in Get-ChildItem -LiteralPath $top.FullName -Directory -Recurse -Depth 7 -Force -Filter $Skill -ErrorAction SilentlyContinue){
   if($dir.FullName -match '\\(node_modules|\.git|synced|cache|\.skill-sync)\\'){continue}
   if(Test-Path -LiteralPath (Join-Path $dir.FullName SKILL.md)){$paths.Add($dir.FullName)}
  }
 }
 return @($paths | Sort-Object -Unique)
}
function Set-CentralSkillLinks([string]$Skill,[string]$Source,[string[]]$Targets,[switch]$RemoverDuplicatas,[switch]$Planejar) {
 $Source=Resolve-CentralSkillPath $Source
 if(!(Get-Command Get-SyncManifest -ErrorAction SilentlyContinue)){. (Join-Path $PSScriptRoot sync_guard.ps1)}
 $registry=Join-Path $env:USERPROFILE ".skill-sync\$Skill.json"
 $prior=@{};if(Test-Path -LiteralPath $registry){$saved=Get-Content -LiteralPath $registry -Raw | ConvertFrom-Json;if((Test-Path -LiteralPath $saved.Source) -and (Resolve-CentralSkillPath $saved.Source) -ne $Source){throw "Source already registered: $($saved.Source). Reconcile before changing the source."};foreach($p in $saved.Files.PSObject.Properties){$prior[$p.Name]=$p.Value}}
 $sourceMap=Get-SyncManifest $Source
 $replace=[Collections.Generic.List[string]]::new()
 $checkedMaps=@{}
 foreach($target in $Targets){
  $full=[IO.Path]::GetFullPath($target).TrimEnd('\')
  if($full -eq $Source){continue}
  if(!$full.StartsWith($env:USERPROFILE.TrimEnd('\')+'\',[StringComparison]::OrdinalIgnoreCase) -or $full -match '\\(synced|cache|node_modules|\.git)\\' -or (Split-Path $full -Leaf) -ne $Skill){throw "Unsafe destination: $full"}
  if(Test-Path -LiteralPath $full){
   if((Resolve-CentralSkillPath $full) -eq $Source){continue}
   $item=Get-Item -LiteralPath $full -Force
   if($item.Attributes -band [IO.FileAttributes]::ReparsePoint){throw "Link points elsewhere: $full"}
   $secrets=@(Get-ChildItem -LiteralPath $full -Recurse -File -Force | Where-Object {$_.Name -match '^\.env' -or $_.Extension -eq '.key'})
   if($secrets.Count){throw "Local credentials must be preserved outside the skill before conversion: $full"}
   $map=Get-SyncManifest $full
   $checkedMaps[$full]=$map
   foreach($rel in $prior.Keys){if($sourceMap.ContainsKey($rel) -and !$map.ContainsKey($rel)){throw "Local deletion requires reconciliation: $full\$rel"}}
   foreach($rel in $map.Keys){
    if($rel -eq '.git'){continue}
    if(!$sourceMap.ContainsKey($rel)){throw "Exclusive file must be reconciled: $full\$rel"}
    if($map[$rel] -ne $sourceMap[$rel] -and (!$prior.ContainsKey($rel) -or $map[$rel] -ne $prior[$rel])){throw "Exclusive edit must be reconciled: $full\$rel"}
   }
   # Never delete a checkout or unexamined reparse point.
   $special=@(Get-ChildItem -LiteralPath $full -Directory -Force -Recurse | Where-Object {($_.Attributes -band [IO.FileAttributes]::ReparsePoint) -or $_.Name -eq '.git' -or $_.Name -eq 'node_modules'})
   if($special.Count){throw "Preserve runtime/repository/link before replacing $full : $($special.FullName -join ', ')"}
  }
  if((Test-Path -LiteralPath $full) -and !$RemoverDuplicatas -and !$Planejar){throw "Use the Desktop BAT to convert the existing copy: $full"}
  $replace.Add($full)
 }
 if($Planejar){Write-Output "[PLAN OK] $Skill : $($replace.Count) conversions, $($Targets.Count) accesses, source $Source";return}
 # Entire inventory is checked before replacing the first directory.
 foreach($full in $replace){
  $parent=Split-Path $full -Parent;New-Item -ItemType Directory -Path $parent -Force | Out-Null
  if(Test-Path -LiteralPath $full){
   $latest=Get-SyncManifest $full
   $expected=$checkedMaps[$full]
   if(!$expected -or $latest.Count -ne $expected.Count){throw "Directory changed after the check: $full"}
   foreach($rel in $expected.Keys){if($latest[$rel] -ne $expected[$rel]){throw "File changed after the check: $full\$rel"}}
   Remove-Item -LiteralPath $full -Recurse -Force
  }
  try{New-Item -ItemType Junction -Path $full -Target $Source | Out-Null}catch{throw "Link creation failed at $full; source is preserved at $Source. Retry installer. $_"}
 }
 foreach($target in $Targets){if((Resolve-CentralSkillPath $target) -ne $Source){throw "Incorrect link: $target"}}
 @{Source=$Source;Mode='central-junction';Targets=$Targets;Files=$sourceMap;VerifiedUtc=[DateTime]::UtcNow.ToString('o')} | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath $registry -Encoding utf8
 Write-Output "[OK] $Skill : $($Targets.Count) local paths reference one source: $Source"
}
