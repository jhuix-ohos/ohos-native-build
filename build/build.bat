@echo OFF

set "FullScriptPath=%~dp0"

python "%FullScriptPath%build.py" %*
if %errorlevel% neq 0 goto error

exit /b

:error
echo FAILED
exit /b 1
