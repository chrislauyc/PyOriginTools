@echo OFF
python update_version.py
cd ..
echo.
echo    You are are about to UPLOAD to PyPi!
echo.
pause
python setup.py sdist upload_docs
echo.
echo    About to update the GitHub with this new version.
echo.
pause
:: requires you add the path to git.exe to your system path.
:: I installed the GitHub desktop client for Windows, so it's in the folder:
:: C:\Users\swharden\AppData\Local\GitHub\PortableGit_d7effa1a4a322478cd29c826b52a0c118ad3db11\cmd\
:: git-cmd.exe commit -m "Update to version v$1"