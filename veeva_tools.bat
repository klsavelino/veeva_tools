@ECHO OFF
CALL P:\Anaconda3\Scripts\activate.bat
python %~dp0tools\cli.py %*
