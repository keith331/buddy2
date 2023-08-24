@echo off
echo | set /p dummyVar="CONNECT ETHERNET CABLE INTO DUT"
:start
ping 10.10.10.10 -w 1000 -n 1 -S 10.10.10.23 | findstr /R /c:"Minimum"
if %errorlevel% == 1 (
goto fail
) else (
echo | set /p dummyVar="."
REM timeout /t 1
goto start
)
:fail
exit