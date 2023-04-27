@echo off
title Simple Neural Network Training Platform

:while
echo ------------------------------
echo Choice an option:
echo 1) Enter Virtual Environment
echo 2) Environment Install
echo 3) Run Flask Server
echo 4) Run test with coverage
echo 5) Exit
echo ------------------------------

set /p choice=Input your choice:
if %choice%==1 (
    goto :EnterVirtual
) else if %choice%==2 (
    goto :EnvironmentInstall
) else if %choice%==3 (
    goto :RunFlask
) else if %choice%==4 (
    goto :RunTest
) else if %choice%==5 (
    goto :Finish
) else (
    goto :while
)

:EnterVirtual
python -m pipenv shell
goto :while

:EnvironmentInstall
pipenv install
goto :while

:RunFlask
flask Run
goto :while

:RunTest
pytest --cov
goto :while

:Finish
echo See you next time!