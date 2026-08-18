import json
import os

def darwin_init(args):
    path = '.darwin'
    if os.path.exists(path):
        print("Darwin repository already initialised")
        return

    os.mkdir(path)

    directories = ['objects', 'refs']
    for item in directories:
        os.mkdir(f"{path}/{item}")

    with open(f"{path}/config", "x"): # 'x' creates a file if it doesnt alr exist
        pass

    with open(f"{path}/index", "w") as f:
        f.write(json.dumps({})) # empty dictionary because it starts with 0 tracked files

    print("Darwin repository initialised")