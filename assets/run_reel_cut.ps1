# run_reel_cut.ps1 - /designer-mestre modules\video.md: runs a script of the cut engine with the right environment.
# Applies the resources from D:\Recursos IA (like assets\resources.py), finds the video in Original\ and writes to Trabalho\reel\cut.
# Usage: powershell -File run_reel_cut.ps1 -Project "<delivery folder>" 1-takes.py "{VIDEO}" "{OUT}"
#      {VIDEO} = first .mp4 of <Project>\Original (or -Video) · {OUT} = <Project>\Trabalho\reel\cut
param(
  [Parameter(Mandatory = $true)][string]$Project,
  [string]$Video,
  [Parameter(Mandatory = $true, Position = 0)][string]$Script,
  [Parameter(ValueFromRemainingArguments = $true)][string[]]$Rest
)
$ErrorActionPreference = 'Stop'
$R = 'D:\Recursos IA'
$env:PYTHONUTF8 = '1'

# tools: GPU before CPU
$ff = Join-Path $R 'Ferramentas\ffmpeg\bin'
$wc = Join-Path $R 'Ferramentas\whisper.cpp-cuda'
if (-not (Test-Path (Join-Path $wc 'whisper-cli.exe'))) { $wc = Join-Path $R 'Ferramentas\whisper.cpp' }
$env:PATH = "$ff;$wc;" + $env:PATH
$model = Get-ChildItem (Join-Path $R 'Modelos\whisper') -Filter 'ggml-*.bin' -ErrorAction SilentlyContinue | Sort-Object Length -Descending | Select-Object -First 1
if ($model -and -not $env:WHISPER_MODEL) { $env:WHISPER_MODEL = $model.FullName }
if (-not $env:CHROME) {
  foreach ($c in 'C:\Program Files\Google\Chrome\Application\chrome.exe', (Join-Path $R 'Ferramentas\chrome\chrome.exe')) {
    if (Test-Path $c) { $env:CHROME = $c; break }
  }
}

if (-not $Video) {
  $v = Get-ChildItem -LiteralPath (Join-Path $Project 'Original') -Filter '*.mp4' -ErrorAction SilentlyContinue | Select-Object -First 1
  if ($v) { $Video = $v.FullName }
}
$out = Join-Path $Project 'Trabalho\reel\cut'
New-Item -ItemType Directory -Force $out | Out-Null

$S = Join-Path $env:USERPROFILE '.claude\skills\designer-mestre\engines\reel\cut\scripts'
$a = @()
foreach ($x in $Rest) { $a += $x.Replace('{VIDEO}', $Video).Replace('{OUT}', $out) }
Write-Host "whisper-cli: $wc | model: $($env:WHISPER_MODEL)"
& python (Join-Path $S $Script) @a
exit $LASTEXITCODE
