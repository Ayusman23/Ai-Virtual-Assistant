@echo off
set ADB_PATH=".\platform-tools\adb.exe"

echo Disconnecting old connections...
%ADB_PATH% disconnect
echo Setting up connected device
%ADB_PATH% tcpip 5555
echo Waiting for device to initialize
timeout 3
FOR /F "tokens=2" %%G IN ('%ADB_PATH% shell ip addr show wlan0 ^|find "inet "') DO set ipfull=%%G
FOR /F "tokens=1 delims=/" %%G in ("%ipfull%") DO set ip=%%G
echo Connecting to device with IP %ip%...
%ADB_PATH% connect %ip%

rem Fallback static connection
set DEVICE_IP=192.0.0.4
set ADB_PORT=5555

echo Restarting ADB server...
%ADB_PATH% kill-server
%ADB_PATH% start-server

echo Connecting to fallback IP %DEVICE_IP%...
%ADB_PATH% connect %DEVICE_IP%:%ADB_PORT%
