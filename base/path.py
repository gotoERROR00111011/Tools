import os

from glob import glob

def mkdir(path: str) -> None: 
    """[summary]

    Args:
        path (str): [description]
    """
    if not os.path.exists(path):
        os.mkdir(path)

def get_dirs(path: str) -> list:
    dirs = [path]
    for d in dirs:
        for filename in os.listdir(d):
            filepath = os.path.join(d, filename)
            if os.path.isdir(filepath):
                dirs.append(filepath)
    return dirs

def get_files(path: str, extention: str="*") -> list:     
    files = []
    for filename in glob(os.path.join(path, extention)):
        files.append(filename)
    return files


