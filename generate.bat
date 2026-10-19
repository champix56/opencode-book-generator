@echo off
setlocal
set "ROOT=%~dp0"
where py >nul 2>nul
if not errorlevel 1 goto use_py
where python >nul 2>nul
if errorlevel 1 (echo Python 3 est requis. 1>&2 & exit /b 127)
python "%ROOT%generators\bookgen.py" %*
exit /b %errorlevel%
:use_py
py -3 "%ROOT%generators\bookgen.py" %*
exit /b %errorlevel%
