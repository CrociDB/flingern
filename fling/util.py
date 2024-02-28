import os
import shutil

def path_relative_from(path, relative):
    common_path = os.path.commonpath([path, relative])
    p = path.replace(common_path, "")
    if p and p[0] == "/": p = p[1:]
    return p

