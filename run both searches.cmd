@echo off
pushd "%~dp0"
rem Run PC searches directly (unbuffered) so output appears in this console
echo.
echo =========================
echo Starting PC Search
echo =========================
py -3 -u search_pc.py %*
if errorlevel 1 (
	echo.
	echo PC search exited with code %ERRORLEVEL%.
) else (
	echo.
	echo PC search completed successfully.
)

rem Run Mobile searches directly (unbuffered) so output appears in this console
echo.
echo ===========================
echo Starting Mobile Search
echo ===========================
py -3 -u search_mobile.py %*
if errorlevel 1 (
	echo.
	echo Mobile search exited with code %ERRORLEVEL%.
) else (
	echo.
	echo Mobile search completed successfully.
)

echo.
pause
popd
exit /b 0