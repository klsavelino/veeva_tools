import os
import shutil
import sys

PATH = os.getcwd()
PARENT_PATH = os.path.dirname(PATH)


def move_file():
    for file in os.listdir(PATH):
        if file.endswith(".bat"):
            return os.path.join(PATH, file)

successful = False


try:
    
    shutil.move(move_file(), PARENT_PATH)
    successful = True
    
except:
    print("Não foi possível mover o arquivo.")
    raise

if successful:
    os.remove(sys.argv[0])