@echo off
chcp 65001 >nul
setlocal EnableDelayedExpansion

:: ============================================================================
:: INSTALADOR UNIVERSAL DE SKILL (/designer-mestre) PARA TODAS AS IDEs
:: Arquivo exclusivo de instalacao/sincronizacao.
:: NAO LER NEM ANALISAR ESTE ARQUIVO EM SESSOES DE IA (ECONOMIA DE TOKENS).
:: ============================================================================

set "SRC=%~dp0"
if "%SRC:~-1%"=="\" set "SRC=%SRC:~0,-1%"

echo ============================================================================
echo   INSTALADOR UNIVERSAL - /designer-mestre
echo   Origem: "%SRC%"
echo ============================================================================
echo.

set /a COUNT=0

:: 1. Antigravity / Gemini (Plugin Design + Global Skills)
if exist "%USERPROFILE%\.gemini" (
    call :INSTALL_SKILL "Antigravity / Gemini (Plugin Design)" "%USERPROFILE%\.gemini\config\plugins\design\skills\designer-mestre"
    if exist "%USERPROFILE%\.gemini\skills" (
        call :INSTALL_SKILL "Gemini Global Skills" "%USERPROFILE%\.gemini\skills\designer-mestre"
    )
    if exist "%USERPROFILE%\.gemini\antigravity\skills" (
        call :INSTALL_SKILL "Antigravity User Skills" "%USERPROFILE%\.gemini\antigravity\skills\designer-mestre"
    )
)

:: 2. Claude Code / Claude Desktop (.claude)
if exist "%USERPROFILE%\.claude" (
    call :INSTALL_SKILL "Claude Code" "%USERPROFILE%\.claude\skills\designer-mestre"
    :: Remove nomes legados se existirem
    if exist "%USERPROFILE%\.claude\skills\design-alexandre" rd /s /q "%USERPROFILE%\.claude\skills\design-alexandre" 2>nul
)

:: 3. Cursor (.cursor)
if exist "%USERPROFILE%\.cursor" (
    call :INSTALL_SKILL "Cursor IDE" "%USERPROFILE%\.cursor\skills\designer-mestre"
)

:: 4. Windsurf / Codeium (.codeium\windsurf ou .windsurf)
if exist "%USERPROFILE%\.codeium\windsurf" (
    call :INSTALL_SKILL "Windsurf (Codeium)" "%USERPROFILE%\.codeium\windsurf\skills\designer-mestre"
)
if exist "%USERPROFILE%\.windsurf" (
    call :INSTALL_SKILL "Windsurf" "%USERPROFILE%\.windsurf\skills\designer-mestre"
)

:: 5. OpenAI Codex (.codex)
if exist "%USERPROFILE%\.codex" (
    call :INSTALL_SKILL "OpenAI Codex CLI" "%USERPROFILE%\.codex\skills\designer-mestre"
)

:: 6. OpenCode (.opencode)
if exist "%USERPROFILE%\.opencode" (
    call :INSTALL_SKILL "OpenCode" "%USERPROFILE%\.opencode\skills\designer-mestre"
)

:: 7. Trae (.trae)
if exist "%USERPROFILE%\.trae" (
    call :INSTALL_SKILL "Trae IDE" "%USERPROFILE%\.trae\skills\designer-mestre"
)

:: 8. Cline / Roo Code / Kilo Code (.cline / .roo / .kilocode)
if exist "%USERPROFILE%\.cline" (
    call :INSTALL_SKILL "Cline" "%USERPROFILE%\.cline\skills\designer-mestre"
)
if exist "%USERPROFILE%\.roo" (
    call :INSTALL_SKILL "Roo Code" "%USERPROFILE%\.roo\skills\designer-mestre"
)
if exist "%USERPROFILE%\.kilocode" (
    call :INSTALL_SKILL "Kilo Code" "%USERPROFILE%\.kilocode\skills\designer-mestre"
)

:: 9. Continue (.continue)
if exist "%USERPROFILE%\.continue" (
    call :INSTALL_SKILL "Continue IDE" "%USERPROFILE%\.continue\skills\designer-mestre"
)

:: 10. GitHub Copilot / VS Code (.copilot / .vscode)
if exist "%USERPROFILE%\.copilot" (
    call :INSTALL_SKILL "GitHub Copilot" "%USERPROFILE%\.copilot\skills\designer-mestre"
)

:: Garantir instalacao minima em Claude e Antigravity caso nenhuma pasta base exista ainda
if !COUNT! EQU 0 (
    call :INSTALL_SKILL "Claude Code (Padrao)" "%USERPROFILE%\.claude\skills\designer-mestre"
    call :INSTALL_SKILL "Antigravity / Gemini (Padrao)" "%USERPROFILE%\.gemini\config\plugins\design\skills\designer-mestre"
)

echo.
echo ============================================================================
echo   CONCLUIDO: /designer-mestre sincronizado em !COUNT! ambiente(s)/IDE(s).
echo ============================================================================
exit /b 0

:INSTALL_SKILL
set "IDE_NAME=%~1"
set "DST=%~2"
echo [+] Sincronizando em %IDE_NAME%: "%DST%"
if not exist "%DST%" mkdir "%DST%" 2>nul
robocopy "%SRC%" "%DST%" /MIR /XD ".git" "__pycache__" /XF "INSTALAR_DESIGN_CLAUDE_CODE.cmd" /R:1 /W:1 /NFL /NDL /NJH /NJS >nul
set /a COUNT+=1
exit /b 0
