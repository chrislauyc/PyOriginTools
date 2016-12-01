:: this script MSUT be run from inside this folder
@echo OFF

set /p moduleName=<moduleName.txt


echo.
echo   ################################
echo   ### UPDATING VERSION COUNTER ###
echo   ################################
echo.
Timeout /t 3 /nobreak

:: update version.py with the new version and create version.bat
python update_version.py
:: pull the version in from the text file that was generated
set /p version=<version.txt
:: from here on we must be in the root folder
cd ..







echo.
echo   #########################
echo   ### UPLOADING TO PYPI ###
echo   #########################
echo.
Timeout /t 3 /nobreak
python setup.py sdist upload






echo.
echo   ###############################
echo   ### UPGRADING LOCAL PACKAGE ###
echo   ###############################
echo.
Timeout /t 3 /nobreak
pip install --upgrade --no-cache-dir %moduleName%







echo.
echo   ###################################
echo   ### CREATING AND UPLOADING DOCS ###
echo   ###################################
echo.
Timeout /t 3 /nobreak
python setup.py sdist upload_docs





echo.
echo   #################################
echo   ### COMMITTING CHANGES TO GIT ###
echo   #################################
echo.
Timeout /t 3 /nobreak

:: using "git" from the command line may require that you add the path to git.exe to your system path:
:: C:\Users\swharden\AppData\Local\GitHub\PortableGit_d7effa1a4a322478cd29c826b52a0c118ad3db11\cmd\

:: collect all changes made during the build
git add --all
:: now commit those changes
git commit -m "PyPi build %version%"



echo.
echo.
echo.
echo DONE! Remember that a GitHub Sync is required. Launching desktop client...
echo.
"%appdata%\..\Local\GitHub\GitHub.appref-ms"
pause
