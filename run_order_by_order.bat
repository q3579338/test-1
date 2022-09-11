@echo off
setlocal enabledelayedexpansion

for %%i in (*) do (
    set FILE=%%~xi
    echo %%i
    @REM echo !FILE!
    if !FILE! == .lnk (
        @REM 执行完退出，不退出用/k
        start cmd /c "%%i"
        choice /t 5 /d y /n >nul
    ) 
    
)
@REM pause
