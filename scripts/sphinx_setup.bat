@echo off
set /p moduleName=<moduleName.txt
echo this script will initiate your sphinx ../docs/ folder
echo you probably only need to run this once...
echo.
cd ..
sphinx-apidoc -F -o docs %moduleName%
pause