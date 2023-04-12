@ECHO OFF
CALL P:\Anaconda3\Scripts\activate.bat
python %~dp0veeva_tools\tools\cli.py %*
