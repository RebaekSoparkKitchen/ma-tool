
chcp 936
echo on
cd /d %~dp0
cd ..
cd ..
cd EDM-venv\Scripts
call activate
cd ..
cd ..
cd src
cd app
cls
cmd.exe