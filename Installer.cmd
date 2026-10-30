@echo off
chcp 65001 >nul
setlocal

set "INSTALLER=%~dp0Installer.ps1"
if not exist "%INSTALLER%" (
    echo [ERROR] Installer.ps1 not found next to this file.
    pause
    exit /b 1
)

powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%INSTALLER%"
set "RESULT=%ERRORLEVEL%"
echo.
pause
exit /b %RESULT%
