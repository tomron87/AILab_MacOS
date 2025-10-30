@echo off 
title AI Environment Help System 
 
set "HELP_DIR=%~dp0" 
 
:main_menu 
cls 
echo. 
echo ================================================================ 
echo                  AI Environment Help System 
echo ================================================================ 
echo. 
echo Select a help topic: 
echo. 
echo  1. Using Ollama AI Models 
echo  2. Using VS Code with AI Environment 
echo  3. Python Development 
echo  4. Project Examples 
echo  5. Managing Ollama Server 
echo  6. Environment Management 
echo  7. Shutdown Procedures 
echo  8. Useful Tips and Troubleshooting 
echo. 
echo  9. Show All Topics (Full Guide) 
echo  0. Exit Help System 
echo. 
echo ================================================================ 
echo. 
set /p choice="Enter your choice (0-9): " 
 
if "%choice%"=="1" call :show_help "1_ollama_models.txt" 
if "%choice%"=="2" call :show_help "2_vscode_usage.txt" 
if "%choice%"=="3" call :show_help "3_python_development.txt" 
if "%choice%"=="4" call :show_help "4_project_examples.txt" 
if "%choice%"=="5" call :show_help "5_manage_ollama.txt" 
if "%choice%"=="6" call :show_help "6_environment_management.txt" 
if "%choice%"=="7" call :show_help "7_shutdown_procedures.txt" 
if "%choice%"=="8" call :show_help "8_useful_tips.txt" 
if "%choice%"=="9" call :show_all_help 
if "%choice%"=="0" goto :exit_help 
 
echo. 
echo Invalid choice. Please try again. 
pause 
goto :main_menu 
 
:show_help 
cls 
echo. 
echo ================================================================ 
echo                     AI Environment Help 
echo ================================================================ 
echo. 
if exist "%HELP_DIR%%~1" ( 
    type "%HELP_DIR%%~1" 
) else ( 
    echo ERROR: Help file "%~1" not found. 
    echo Please ensure all help files are in the help directory. 
) 
echo. 
echo ================================================================ 
echo. 
pause 
goto :main_menu 
 
:show_all_help 
cls 
echo. 
echo ================================================================ 
echo                   COMPLETE AI ENVIRONMENT GUIDE 
echo ================================================================ 
echo. 
 
for %%f in ("%HELP_DIR%*.txt") do ( 
    echo. 
    echo ---------------------------------------------------------------- 
    type "%%f" 
    echo ---------------------------------------------------------------- 
) 
 
echo. 
echo ================================================================ 
echo                     End of Complete Guide 
echo ================================================================ 
echo. 
pause 
goto :main_menu 
 
:exit_help 
echo. 
echo Exiting Help System... 
exit /b 0 
