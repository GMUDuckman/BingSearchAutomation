@echo off
REM Check for /nowait and /shutdown switches
set NOWAIT=false
set SHUTDOWN=false
set SHUTDOWNTIME=60
set ONLYMOBILE=false
set ONLYPC=false
for %%i in (%*) do (
    if /I "%%i"=="/nowait" set NOWAIT=true
    if /I "%%i"=="/shutdown" set SHUTDOWN=true
    if /I "%%i"=="/onlymobile" set ONLYMOBILE=true
    if /I "%%i"=="/onlypc" set ONLYPC=true
    echo %%i | findstr /I /B /C:"/shutdowntime:" >nul
    if not errorlevel 1 (
        for /f "tokens=2 delims=:" %%a in ("%%i") do set SHUTDOWNTIME=%%a
    )
)

if "%NOWAIT%"=="true" (
    REM Bypass random delay
    echo Bypassing random timer. Running scripts immediately...
) else (
    REM Calculate a random delay between 0 and 10800 seconds (3 hours)
    set /a rand=%RANDOM% * 1800 / 32768
    REM Wait for the random delay
    timeout /t %rand% /nobreak
)
REM Run the Python script
python run_both_searches.py %ONLYMOBILE% %ONLYPC%

if "%SHUTDOWN%"=="true" (
    echo The computer will shut down in %SHUTDOWNTIME% seconds. Save your work!
    shutdown /s /t %SHUTDOWNTIME%
) 