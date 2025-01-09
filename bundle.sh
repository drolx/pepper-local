#!/bun/sh

pyinstaller cli.py --onefile --name pepper-local # --hiddenimport=aiohttp --hiddenimport=crontab
