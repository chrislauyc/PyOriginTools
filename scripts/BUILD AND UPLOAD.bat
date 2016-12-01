:: this script MSUT be run from inside this folder
@echo OFF

:: update version.py with the new version and create version.bat
python update_version.py

:: pull the version in from the text file that was generated
set /p version=<version.txt

:: now we MUST go to the root of this package
cd ..
echo.
echo    You are are about to UPLOAD version %version% to PyPi 
echo.
pause
python setup.py sdist upload
echo.
echo   Now uploading documentation...
echo.
python setup.py upload_docs --upload-dir=docs/html

:: using "git" from the command line may require that you add the path to git.exe to your system path:
:: C:\Users\swharden\AppData\Local\GitHub\PortableGit_d7effa1a4a322478cd29c826b52a0c118ad3db11\cmd\
echo.
echo    About to update the GitHub with Version %version%
echo.
pause

:: collect all changes made during the build
git add --all
git commit -m "PyPi build %version%"
echo.
echo DONE! GitHub Sync required.
echo.

:: launching the desktop client
::"C:\Users\swharden\AppData\Local\GitHub\GitHub.appref-ms"
pause
