@echo off
taskkill /f /im explorer.exe
cls
color a
set code=""

:code
set /p code="Gib den Administratorcode ein: "
if "%code%"== "12345" goto correct
if NOT "%code%"== "12345" goto wrong

:correct
echo Zugriff gewaehrt!
start explorer
exit

:wrong
echo Zugriff verweigert!
echo Versuche es erneut: 
goto code


//codes:

//2t38fw9dW0f!g
