pyinstaller simple_discord.py -w --onefile
rm -fr "__pycache__"
rm -fr "build/*"
rm -fr "simple_discord.spec"
mv "dist/simple_discord.exe ../"
rm -fr "dist/"