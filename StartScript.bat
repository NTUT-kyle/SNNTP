@echo off
title Simple Neural Network Training Platform
echo Choice an option:
echo 1) Enter Virtual Environment
echo 2) Environment Setting
echo 3) Run Flask Server
echo 4) Exit

choice /c 1234 /n /m "Input your choice:"
set choice=%errorlevel%
if %choice%==1 python -m pipenv shell
if %choice%==2 echo Environment Setting TBD!
if %choice%==3 flask run
if %choice%==4 exit