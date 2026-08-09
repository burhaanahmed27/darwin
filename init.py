import json
import os
import argparse
import hashlib

# function that encodes the file name to its hash
def create_objectID(file_content):
    my_hash = hashlib.sha256(file_content).hexdigest()
    return my_hash

# function that creates a file for it in objects if not already exists
def create_path(my_hash, file_content):
    full_path = f".darwin/objects/{my_hash}"

    with open(full_path, "xb") as f:
        f.write(file_content)

def check_objectID_exists(file_content):
    return os.path.exists(f".darwin/objects/{create_objectID(file_content)}")

def darwin_add(args):
    file_name = args.path
    file_dictionary = {}

    # EITHER - loading the dictionary from index - OR - creating an empty dictionary
    try:
        with open(".darwin/index", "r") as f:
            file_dictionary = json.load(f)
    except FileNotFoundError:
        print("You need to create a repository first")
        return

    # staging all files
    if file_name == ".":
        for root, subFolder, files in os.walk("."): # here, "." means your current working directory
            if ".darwin" in subFolder:
                subFolder.remove(".darwin")

            for f in files:
                file_path = os.path.join(root, f)
                #print(file_path)
                stage_file(file_path, file_dictionary)

    # staging one file
    elif not os.path.exists(file_name):
        print("Invalid file name")
    else:
        stage_file(file_name, file_dictionary)

def stage_file(file_name, file_dictionary):
    # read the file contents and check if the object ID already exists
    with open(file_name, "rb") as f:
        file_content = f.read()

    # if the object ID doesn't exist, we need to create a hash for it
    if not check_objectID_exists(file_content):
        create_path(create_objectID(file_content), file_content)

    # we then need to map the file name to the hash in our dictionary
    file_dictionary[file_name] = create_objectID(file_content)

    # send the data to index
    json_data = json.dumps(file_dictionary)
    with open(".darwin/index", "w") as f:
        f.write(json_data)


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

def main():
    parser = argparse.ArgumentParser() # object that can read arguments from command line
    subparsers = parser.add_subparsers(dest="command", required=True) # an object to register commands like init, add etc
        #required = True means subcommands are required
        #dest = "command" stores the command name in args.command

    init_parser = subparsers.add_parser('init', help = 'Create a local Git repository')
    init_parser.set_defaults(func=darwin_init) #associate the init command to the function

    add_parser = subparsers.add_parser('add', help = 'Add an object to the repository')
    add_parser.add_argument('path')
    add_parser.set_defaults(func=darwin_add) #associate the add command to the function

    args = parser.parse_args() #returns an object that contains the user's argument(s)
    args.func(args) #the args.func attribute stores the associated method

if __name__ == "__main__":
    main()
