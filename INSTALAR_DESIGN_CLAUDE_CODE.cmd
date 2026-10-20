@echo off
chcp 65001 >nul
setlocal EnableExtensions
title Instalar /designer-mestre v15 (Claude Code + Antigravity)
set "ORIGEM=%~dp0"
set "DEST_CLAUDE=%USERPROFILE%\.claude\skills\designer-mestre"
set "DEST_AGY=%USERPROFILE%\.gemini\config\plugins\design\skills\designer-mestre"

echo.
echo  ==============================================
echo   Instalando /designer-mestre v15
echo  ==============================================

if not exist "%ORIGEM%SKILL.md" (
  echo  ERRO: SKILL.md nao encontrado na pasta do agente.
  pause & exit /b 1
)

rem --- 1. Instala a skill (copia limpa) ---
for %%D in ("%DEST_CLAUDE%" "%DEST_AGY%") do (
  if exist "%%~D" rmdir /s /q "%%~D"
  mkdir "%%~D"
  copy /y "%ORIGEM%SKILL.md" "%%~D\SKILL.md" >nul
  if exist "%ORIGEM%README.md" copy /y "%ORIGEM%README.md" "%%~D\README.md" >nul
  if exist "%ORIGEM%CREDITOS_HTML.md" copy /y "%ORIGEM%CREDITOS_HTML.md" "%%~D\CREDITOS_HTML.md" >nul
  for %%M in (modulos assets engines references figma_engine pen_engine) do (
    if exist "%ORIGEM%%%M" robocopy "%ORIGEM%%%M" "%%~D\%%M" /MIR /NFL /NDL /NJH /NJS /NP >nul
  )
  robocopy "%ORIGEM%Clientes\_TEMPLATE_CLIENTE" "%%~D\Clientes\_TEMPLATE_CLIENTE" /MIR /NFL /NDL /NJH /NJS /NP >nul
)
echo  [ok] v15 instalada em:
echo       %DEST_CLAUDE%
echo       %DEST_AGY%

rem --- 1b. Requisitos de imagem (tudo local) ---
echo.
where magick >nul 2>&1 && (echo  [ok] ImageMagick encontrado) || (echo  [!] ImageMagick ausente. Instale com:  winget install ImageMagick.ImageMagick)
curl -s -m 3 http://127.0.0.1:9000/ping >nul 2>&1 && (echo  [ok] Easy Diffusion respondendo em 127.0.0.1:9000) || (echo  [i] Easy Diffusion fechado ou nao instalado. Para gerar imagem: abra o Start Stable Diffusion UI ^(motor v4 + FLUX.2 klein 4B^).)

rem --- 2. Requisitos de video (so verifica; instala so com "s") ---
echo.
where ffmpeg >nul 2>&1 && (echo  [ok] ffmpeg encontrado) || (echo  [!] ffmpeg ausente. Instale com:  winget install Gyan.FFmpeg)
where python >nul 2>&1
if errorlevel 1 (
  echo  [!] Python ausente. Instale o Python 3.10+ ^(python.org^) para legenda de video e o motor uiux.
) else (
  python -c "import faster_whisper" >nul 2>&1 && (echo  [ok] faster-whisper encontrado) || (
    set /p RESP="  Instalar faster-whisper agora para legendar videos? (s/n) "
    call :pipwhisper
  )
)
echo.
pause
endlocal
exit /b 0

:pipwhisper
if /i "%RESP%"=="s" (
  python -m pip install --upgrade faster-whisper
) else (
  echo  Pulado. Depois: python -m pip install faster-whisper
)
exit /b 0
