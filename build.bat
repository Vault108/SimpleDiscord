pyinstaller simple_discord.py -w --onefile
rd /S /Q "__pycache__/" 
rd /S /Q "build\"
rd /S /Q "simple_discord.spec"
move .\dist\simple_discord.exe .\
rd /S /Q "dist/"