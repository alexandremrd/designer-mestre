@echo off
chcp 65001 >nul
setlocal

set "INSTALLER=%~dp0Instalador.ps1"
if not exist "%INSTALLER%" (
    echo [ERRO] Instalador.ps1 nao encontrado ao lado deste arquivo.
    pause
    exit /b 1
)

powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%INSTALLER%"
set "RESULT=%ERRORLEVEL%"
echo.
pause
exit /b %RESULT%
