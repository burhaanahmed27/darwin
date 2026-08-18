import json
import os
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
