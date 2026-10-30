# Local installation uses one source and NTFS junctions, never mirrored copies.
param([switch]$Sim,[switch]$RemoverDuplicatas)
$ErrorActionPreference='Stop'
. (Join-Path $PSScriptRoot 'central_skill.ps1')
$source=Resolve-CentralSkillPath $PSScriptRoot
$registry=Join-Path $env:USERPROFILE '.skill-sync\designer-mestre.json'
if(Test-Path -LiteralPath $registry){
 $registered=(Get-Content -LiteralPath $registry -Raw | ConvertFrom-Json).Source
 if(Test-Path -LiteralPath $registered){$source=Resolve-CentralSkillPath $registered}
}
$targets=@(Get-CentralSkillTargets 'designer-mestre')
Set-CentralSkillLinks -Skill 'designer-mestre' -Source $source -Targets $targets -RemoverDuplicatas:$RemoverDuplicatas
foreach($shortcut in Get-ChildItem -LiteralPath (Join-Path $source 'shortcuts') -Directory){
 $shortcutTargets=@($targets | Where-Object {(Split-Path (Split-Path $_ -Parent) -Leaf) -eq 'skills'} | ForEach-Object {Join-Path (Split-Path $_ -Parent) $shortcut.Name})
 Set-CentralSkillLinks -Skill $shortcut.Name -Source $shortcut.FullName -Targets $shortcutTargets -RemoverDuplicatas:$RemoverDuplicatas
}
Write-Host '[OK] Single source and shortcuts checked. Reload the skills in the AIs.'
