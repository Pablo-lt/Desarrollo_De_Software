@echo off
set VAR_CONTEXT=%1
if "%VAR_CONTEXT%"=="production" (
    set VAR_CONTEXT=production
) else (
    set VAR_CONTEXT=development
)
echo environment set to: %VAR_CONTEXT%
set FLASK_CONTEXT=%VAR_CONTEXT%
python app.py