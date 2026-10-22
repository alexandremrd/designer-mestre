$ErrorActionPreference = 'Stop'

$source = $PSScriptRoot
$skillFile = Join-Path $source 'SKILL.md'
if (-not (Test-Path -LiteralPath $skillFile -PathType Leaf)) {
    Write-Host "[ERRO] SKILL.md nao encontrado em '$source'." -ForegroundColor Red
    Write-Host 'Extraia o projeto completo e execute Instalador.cmd novamente.'
    exit 1
}

$homePath = $env:USERPROFILE
$targets = @(
    [pscustomobject]@{
        Name = 'Global Agents Skills (Codex, Copilot e compatibilidade)'
        Path = Join-Path $homePath '.agents\skills\designer-mestre'
    }
)

$optionalTargets = @(
    @{ Root = '.gemini'; Name = 'Gemini CLI'; Path = '.gemini\skills\designer-mestre' },
    @{ Root = '.gemini\antigravity'; Name = 'Antigravity'; Path = '.gemini\antigravity\skills\designer-mestre' },
    @{ Root = '.claude'; Name = 'Claude Code'; Path = '.claude\skills\designer-mestre' },
    @{ Root = '.cursor'; Name = 'Cursor'; Path = '.cursor\skills\designer-mestre' },
    @{ Root = '.codeium\windsurf'; Name = 'Windsurf'; Path = '.codeium\windsurf\skills\designer-mestre' }
)

foreach ($entry in $optionalTargets) {
    $root = Join-Path $homePath $entry.Root
    if (Test-Path -LiteralPath $root -PathType Container) {
        $targets += [pscustomobject]@{
            Name = $entry.Name
            Path = Join-Path $homePath $entry.Path
        }
    }
}

$legacyTargets = @(
    @{ Name = 'Copia legada Gemini'; Path = '.gemini\config\plugins\design\skills\designer-mestre' },
    @{ Name = 'Copia legada Codex'; Path = '.codex\skills\designer-mestre' },
    @{ Name = 'Copia legada Copilot'; Path = '.copilot\skills\designer-mestre' },
    @{ Name = 'Copia legada Windsurf'; Path = '.windsurf\skills\designer-mestre' },
    @{ Name = 'Copia legada OpenCode'; Path = '.opencode\skills\designer-mestre' },
    @{ Name = 'Copia legada Trae'; Path = '.trae\skills\designer-mestre' },
    @{ Name = 'Copia legada Cline'; Path = '.cline\skills\designer-mestre' },
    @{ Name = 'Copia legada Roo Code'; Path = '.roo\skills\designer-mestre' },
    @{ Name = 'Copia legada Kilo Code'; Path = '.kilocode\skills\designer-mestre' },
    @{ Name = 'Copia legada Continue'; Path = '.continue\skills\designer-mestre' }
)

foreach ($entry in $legacyTargets) {
    $path = Join-Path $homePath $entry.Path
    if ((Test-Path -LiteralPath $path -PathType Container) -and $path -notin $targets.Path) {
        $targets += [pscustomobject]@{
            Name = $entry.Name
            Path = $path
        }
    }
}

function Get-SkillSourceFiles {
    param([string]$Root)

    $excludedDirectoryPattern = '^(\.git|node_modules|__pycache__|_backup_.*)$'
    $pendingDirectories = [System.Collections.Generic.Stack[string]]::new()
    $files = [System.Collections.Generic.List[System.IO.FileInfo]]::new()
    $pendingDirectories.Push($Root)

    while ($pendingDirectories.Count -gt 0) {
        $currentDirectory = $pendingDirectories.Pop()
        foreach ($item in Get-ChildItem -LiteralPath $currentDirectory -Force) {
            if (($item.Attributes -band [System.IO.FileAttributes]::ReparsePoint) -ne 0) {
                continue
            }

            if ($item.PSIsContainer) {
                if ($item.Name -notmatch $excludedDirectoryPattern) {
                    $pendingDirectories.Push($item.FullName)
                }
                continue
            }

            # Credenciais nunca entram no pacote instalado.
            if ($item.Name -ne 'INSTALAR_DESIGN_CLAUDE_CODE.cmd' -and $item.Name -notmatch '^\.env' -and $item.Extension -ne '.key') {
                $files.Add($item)
            }
        }
    }

    return $files.ToArray()
}

$sourceFiles = @(Get-SkillSourceFiles -Root $source)

if ($sourceFiles.Count -eq 0) {
    Write-Host '[ERRO] Nenhum arquivo de skill foi encontrado para instalar.' -ForegroundColor Red
    exit 1
}

Write-Host '============================================================'
Write-Host '  INSTALADOR /designer-mestre'
Write-Host "  Origem: $source"
Write-Host '============================================================'
Write-Host ''
Write-Host 'Destinos globais:'
foreach ($target in $targets) {
    Write-Host "  - $($target.Name): $($target.Path)"
}

$confirmation = Read-Host "`nInstalar/sincronizar nesses destinos? [S/N]"
if ($confirmation.Trim() -notmatch '^(s|sim)$') {
    Write-Host 'Instalacao cancelada; nenhum arquivo foi alterado.'
    exit 0
}

$installedTargets = [System.Collections.Generic.List[object]]::new()
$failureCount = 0
foreach ($target in $targets) {
    try {
        $sourceFullPath = [System.IO.Path]::GetFullPath($source).TrimEnd('\')
        $targetFullPath = [System.IO.Path]::GetFullPath($target.Path).TrimEnd('\')
        $sameDirectory = $sourceFullPath.Equals(
            $targetFullPath,
            [System.StringComparison]::OrdinalIgnoreCase
        )

        if (-not $sameDirectory) {
            New-Item -ItemType Directory -Path $target.Path -Force | Out-Null

            foreach ($file in $sourceFiles) {
                $relativePath = $file.FullName.Substring($source.Length).TrimStart('\')
                $destinationFile = Join-Path $target.Path $relativePath
                $destinationDirectory = Split-Path -Parent $destinationFile
                New-Item -ItemType Directory -Path $destinationDirectory -Force | Out-Null
                Copy-Item -LiteralPath $file.FullName -Destination $destinationFile -Force
            }
        }
        else {
            Write-Host "[INFO] A origem ja e o destino global: '$source'."
        }

        $mismatches = @(
            foreach ($file in $sourceFiles) {
                $relativePath = $file.FullName.Substring($source.Length).TrimStart('\')
                $destinationFile = Join-Path $target.Path $relativePath
                if (-not (Test-Path -LiteralPath $destinationFile -PathType Leaf)) {
                    $relativePath
                    continue
                }

                $sourceHash = (Get-FileHash -LiteralPath $file.FullName -Algorithm SHA256).Hash
                $destinationHash = (Get-FileHash -LiteralPath $destinationFile -Algorithm SHA256).Hash
                if ($sourceHash -ne $destinationHash) {
                    $relativePath
                }
            }
        )

        if ($mismatches.Count -gt 0) {
            throw "Verificacao SHA-256 falhou: $($mismatches -join ', ')"
        }

        Write-Host "[OK] $($target.Name): $($sourceFiles.Count) arquivos conferidos por SHA-256."
        $installedTargets.Add($target)
    }
    catch {
        Write-Host "[ERRO] $($target.Name) em '$($target.Path)': $($_.Exception.Message)" -ForegroundColor Red
        $failureCount++
    }
}

$imageScript = Join-Path $source 'assets\tratar_imagem.mjs'
if ($installedTargets.Count -gt 0 -and (Test-Path -LiteralPath $imageScript -PathType Leaf)) {
    $npm = Get-Command 'npm.cmd' -ErrorAction SilentlyContinue
    if ($null -eq $npm) {
        Write-Host '[AVISO] npm.cmd nao encontrado; sharp opcional nao foi instalado.'
    }
    else {
        $answer = Read-Host "`nInstalar sharp opcional para tratar_imagem.mjs? Isso baixa um pacote npm por destino. [S/N]"
        if ($answer.Trim() -match '^(s|sim)$') {
            foreach ($target in $installedTargets) {
                $assetsPath = Join-Path $target.Path 'assets'
                $sharpPath = Join-Path $assetsPath 'node_modules\sharp'
                if (Test-Path -LiteralPath $sharpPath -PathType Container) {
                    Write-Host "[OK] sharp ja existe em '$assetsPath'."
                    continue
                }

                Write-Host "Instalando sharp em '$assetsPath'..."
                & $npm.Source install --prefix $assetsPath sharp --no-save --no-audit --no-fund --package-lock=false
                if ($LASTEXITCODE -ne 0 -or -not (Test-Path -LiteralPath $sharpPath -PathType Container)) {
                    Write-Host "[ERRO] sharp nao foi instalado em '$assetsPath'." -ForegroundColor Red
                    $failureCount++
                }
                else {
                    Write-Host "[OK] sharp instalado em '$assetsPath'."
                }
            }
        }
        else {
            Write-Host 'sharp opcional nao foi instalado.'
        }
    }
}

Write-Host ''
if ($failureCount -gt 0) {
    Write-Host "[FALHA] $failureCount etapa(s) falharam; consulte os detalhes acima." -ForegroundColor Red
    exit 1
}

Write-Host "[OK] /designer-mestre verificado em $($installedTargets.Count) destino(s)."
Write-Host 'Abra/recarregue a IDE para que ela descubra a skill.'
exit 0
