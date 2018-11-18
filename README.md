# RevShell

A Simple Python 3 Reverse Shell Script


## Usage

- Install required Python packages.

   ```
   pip install -r packages.txt
   ```
- Run the server script.

   ```
   python server.py --port 58777
   ```

- Configure server settings inside **config.json**.

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
  pyinstaller server.py -F -y -i shell.icon  
  ```
  
- Client script, use the `windowed` option to prevent the script from launching a command window

  ```
  pyinstaller client.py -F -y -i shell.icon --windowed
  ```


## Credits

- This script is based on [this article](https://null-byte.wonderhowto.com/how-to/reverse-shell-using-python-0163875/) from WonderHowTo.com
