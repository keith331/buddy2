@echo off
ssh device vpd -l | findstr /B /R /c:"\"serial"