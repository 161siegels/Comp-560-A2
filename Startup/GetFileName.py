import sys
from os import path
from pathlib import Path


def get_file_name() -> str:
    if len(sys.argv) != 2:
        print("Usage: python main.py [TEXT FILENAME]")
        print("For example: \"python3 main.py filename.txt\"")
        exit(1)
    else:
        if path.exists("Files/" + sys.argv[1]):
            return Path("Files/" + sys.argv[1])
        else:
            print("File not found, please make sure it was entered correctly.")
            exit(1)
