@echo off
setlocal enabledelayedexpansion

for %%i in (*) do (
    set FILE=%%~xi
    echo %%i
    @REM echo !FILE!
    if !FILE! == .lnk (
        start cmd /k "%%i"
        choice /t 5 /d y /n >nul
    ) 
    
)
@REM pause
