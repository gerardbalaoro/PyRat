pyinstaller server.py -F -y -i shell.ico --name "PyRatServer" --specpath "build/"
pyinstaller client.py -F -y -i gear.ico --name "PyRatClient" --specpath "build/"
pyinstaller client.py -F -y -i gear.ico --name "PyRatPayload" --specpath "build/" --windowed