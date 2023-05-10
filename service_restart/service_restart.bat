@echo off

setlocal enabledelayedexpansion

set PREFIX=_
for /f "tokens=2 delims=: " %%s in ('sc query state^= all ^| findstr /b /c:"SERVICE_NAME: %PREFIX%"') do (
    set SERVICE_NAME=%%s
    sc query !SERVICE_NAME! | find "RUNNING"
    if !errorlevel! == 0 (
        net stop !SERVICE_NAME!
        net start !SERVICE_NAME!
    ) else (
        net start !SERVICE_NAME!
    )
)

pause