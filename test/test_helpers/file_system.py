import os

def cleanup(filename):
    if os.path.exists(f"{filename}.txt"):
        os.remove(f"{filename}.txt")