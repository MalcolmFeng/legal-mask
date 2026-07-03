@echo off
REM Build legal-mask Windows executable
echo Building legal-mask for Windows...

REM Install dependencies
pip install -r requirements.txt
pip install pyinstaller

REM Build
python build.py

echo.
echo Done! Find legal-mask.exe in the dist\ folder
pause
