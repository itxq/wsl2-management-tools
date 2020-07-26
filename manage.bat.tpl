@echo off
{cmd}
cd /d %~dp0
cd ../
setlocal enabledelayedexpansion
for /f "delims=  tokens=1" %%i in ('netstat -aon ^| findstr "{port}"') do (
set a=%%i
goto js
)
:js
taskkill /f /pid "!a:~71,5!"
python.exe manage.py