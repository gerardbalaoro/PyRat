<h1 align="center">PyRat: ReverseShell</h1>
<p align="center">A Fully Undetectable Python 3 Reverse Shell Script</p>

<hr>

> ## Disclaimer
>
> The author intended this script to be used for educational and research puposes only.



## Usage

- Install required Python packages.

   ```
   pip install -r packages.txt
   ```

- Run the server script.

   ```
   python server.py --port 58777
   ```

- Configure server settings inside **config.ini**.

  ```json
  {
    "host":"127.0.0.1",
    "port":58777
  }

  ```
  
- Run client script in another computer.


## Building Binaries Using PyInstaller

- Server script

  ```bash
  pyinstaller server.py -F -y -i shell.ico --name "RevShellServer" --specpath "build/" 
  ```
  
- Client script, use the `windowed` option to prevent the script from launching a command window

  ```bash
  pyinstaller client.py -F -y -i gear.ico --name "RevShellClient" --specpath "build/"
  pyinstaller client.py -F -y -i gear.ico --name "RevShellPayload" --specpath "build/" --windowed
  ```


## Credits

- This script is based on [this article](https://null-byte.wonderhowto.com/how-to/reverse-shell-using-python-0163875/) from WonderHowTo.com
