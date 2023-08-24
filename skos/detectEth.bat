@echo off
echo | set /p dummyVar="CONNECT ETHERNET CABLE INTO DUT"
:start
ping 10.10.10.10 -w 300 -n 1 -S 10.10.10.23 | findstr /R /c:"TTL"
if %errorlevel% == 1 (
goto fail
) else (
exit
)
:fail
echo | set /p dummyVar="."
goto start