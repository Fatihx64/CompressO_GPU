@echo off
title CompressO-GPU (NVIDIA Accelerated)
cd /d "%~dp0"

echo ====================================================
echo  CompressO - NVIDIA GPU Accelerated Compression
echo ====================================================
echo.

set "PATH=%USERPROFILE%\.cargo\bin;%PATH%"

if exist "src-tauri\target\debug\compressO.exe" (
    echo [INFO] Starting CompressO-GPU...
    start "" "src-tauri\target\debug\compressO.exe"
    exit /b 0
)

echo [INFO] Launching CompressO via Tauri...
cmd /c "npx pnpm tauri dev"
pause
