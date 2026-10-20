@echo off
chcp 65001 >nul
setlocal EnableExtensions
title Instalar /designer-mestre v17 (Claude Code + Antigravity)
set "ORIGEM=%~dp0"
set "DEST_CLAUDE=%USERPROFILE%\.claude\skills\designer-mestre"
set "DEST_AGY=%USERPROFILE%\.gemini\config\plugins\design\skills\designer-mestre"

echo.
echo  ==============================================
echo   Instalando /designer-mestre v17.1 (Autonomo)
echo  ==============================================

if not exist "%ORIGEM%SKILL.md" (
  echo  ERRO: SKILL.md nao encontrado na pasta do agente.
  pause & exit /b 1
)

for %%D in ("%DEST_CLAUDE%" "%DEST_AGY%") do (
  if exist "%%~D" rmdir /s /q "%%~D"
  mkdir "%%~D"
  copy /y "%ORIGEM%SKILL.md" "%%~D\SKILL.md" >nul
  if exist "%ORIGEM%README.md" copy /y "%ORIGEM%README.md" "%%~D\README.md" >nul
  for %%M in (modulos assets engines references figma_engine pen_engine) do (
    if exist "%ORIGEM%%%M" robocopy "%ORIGEM%%%M" "%%~D\%%M" /MIR /NFL /NDL /NJH /NJS /NP >nul
  )
  robocopy "%ORIGEM%Clientes\_TEMPLATE_CLIENTE" "%%~D\Clientes\_TEMPLATE_CLIENTE" /MIR /NFL /NDL /NJH /NJS /NP >nul
)
echo  [ok] /designer-mestre instalado e sincronizado em:
echo       %DEST_CLAUDE%
echo       %DEST_AGY%
echo.
pause
endlocal
exit /b 0
