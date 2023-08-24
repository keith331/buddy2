@echo off

REM read serial
FOR /F "tokens=1-2 delims==" %%I IN ('getSN.bat') DO (set var_serial=%%J)

REM remove quotes from serial
for /f "useback tokens=*" %%a in ('%var_serial%') do set var_serial=%%~a

REM write serial to SC
python writeSN2SC.py %var_serial%

REM set Volume
ssh device amixer sset 'Master' 100%
ssh device amixer sset 'Capture' 25%

REM set DSP of mic (cant edit file system, can only use commands)

REM set DSP of speakers (cant edit file system, can only use commands)

REM set fan speed, lowest except 0 is 2100, using 2100 to get realistic EIN
ssh device sudo ectool pwmsetfanrpm 2100
ssh device sudo ectool pwmgetfanrpm

ssh device mkdir -p /media/recs

REM preload stim
REM scp -i "c:\Users\medma\.ssh\testing_rsa" -o stricthostkeychecking=no -r ./stimFiles/ root@10.10.10.10:/media/
scp -i "%userprofile%\.ssh\testing_rsa" -o stricthostkeychecking=no -r ./stimFiles/ root@10.10.10.10:/media/

註解：
-r 將server文件傳送至本地
-i 指定 testing_rsa 寫入
-o stricthostkeychecking=no 避免在第一次連結裝置使用scp 會出現yes/no中斷自動程序
