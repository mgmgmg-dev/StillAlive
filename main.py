from os import system
from sys import platform

if platform == "darwin": system('open -a Terminal ./assets/launcher.command')
elif platform == "win32": system('start "Still Alive" /d assets /max /realtime "cmd /C launcher.bat"')