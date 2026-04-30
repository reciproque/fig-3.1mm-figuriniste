@echo off

cd /d "%~dp0"

call phidgets\env\Scripts\activate.bat

python phidgets-keyboard.py

:: Pause to keep the window open after script execution (optional)
pause