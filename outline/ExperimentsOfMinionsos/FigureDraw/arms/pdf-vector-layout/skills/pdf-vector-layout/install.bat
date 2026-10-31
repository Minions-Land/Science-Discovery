@echo off
REM Install pdf-vector-layout skill to Codex and/or Claude Code on Windows
REM
REM Usage:
REM   install.bat codex     - install only to Codex
REM   install.bat claude    - install only to Claude Code
REM   install.bat both      - install to both (default)

setlocal

set SKILL_NAME=pdf-vector-layout
set SCRIPT_DIR=%~dp0
set TARGET=%1
if "%TARGET%"=="" set TARGET=both

if "%TARGET%"=="codex" (
    call :install "%USERPROFILE%\.codex\skills" "Codex"
) else if "%TARGET%"=="claude" (
    call :install "%USERPROFILE%\.claude\skills" "Claude Code"
) else if "%TARGET%"=="both" (
    call :install "%USERPROFILE%\.codex\skills" "Codex"
    call :install "%USERPROFILE%\.claude\skills" "Claude Code"
) else (
    echo Usage: %0 [codex^|claude^|both]
    exit /b 1
)

echo.
echo Done. Try invoking the skill by asking:
echo   '请帮我移动 PDF 中的图到页面下方，保持矢量可编辑'
exit /b 0

:install
set TARGET_DIR=%~1
set TARGET_NAME=%~2
if not exist "%TARGET_DIR%" (
    echo Creating %TARGET_DIR%
    mkdir "%TARGET_DIR%"
)
if exist "%TARGET_DIR%\%SKILL_NAME%" (
    echo Removing existing %TARGET_NAME% skill at %TARGET_DIR%\%SKILL_NAME%
    rmdir /s /q "%TARGET_DIR%\%SKILL_NAME%"
)
xcopy /E /I /Q "%SCRIPT_DIR%" "%TARGET_DIR%\%SKILL_NAME%" >nul
del /q "%TARGET_DIR%\%SKILL_NAME%\install.sh" 2>nul
del /q "%TARGET_DIR%\%SKILL_NAME%\install.bat" 2>nul
del /q "%TARGET_DIR%\%SKILL_NAME%\INSTALL.md" 2>nul
echo [OK] Installed to %TARGET_NAME%: %TARGET_DIR%\%SKILL_NAME%
exit /b 0
