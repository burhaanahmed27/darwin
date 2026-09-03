import hashlib
import json
import os

dict = {} # full_path -> DirectoryNode object

# loading the dictionary from index
with open(".darwin/index", "r") as f:
    file_dictionary = json.load(f) # full_path -> hash

class DirectoryNode:
    def __init__(self, file_name, full_path):
        self.file_name = file_name
        self.children = []
        self.full_path = full_path

    def add_child(self, child_file):
        child_file.parent = self
        self.children.append(child_file)

def is_node_created(file_name):
    return file_name in dict

def print_tree(node):
    print(node.file_name)

    for child in node.children:
        print_tree(child)

def create_tree():
    root = DirectoryNode(".", ".")

    for path in file_dictionary:
        parts = os.path.normpath(path).split(os.sep)

        current_node = root

        for part in parts:
            full_path = os.path.normpath(os.path.join(current_node.full_path, part))

            if not is_node_created(full_path): # if it doesn't have a node yet
                new_node = DirectoryNode(part, full_path) # create new node underneath current_node
                current_node.add_child(new_node)
                dict[full_path] = new_node # add it to the dictionary
                current_node = new_node # then move current_node down to that node
            else: # if it does have a node
                current_node = dict[full_path] # move current_node down to that node

    return root

# encoding the tree to its hash
def hash_tree(tree):
    hash_object = hashlib.sha256()

    for child in sorted(tree.children, key=lambda x: x.file_name):
        if child.children == []: # if its a file
            child_hash = file_dictionary[child.full_path] # get the hash from file_dictionary
        else: # if its a folder
            child_hash = hash_tree(child) # recursively call hash_tree(child)

        concatenation = child.file_name + child_hash
        hash_object.update(concatenation.encode())

    return hash_object.hexdigest()

if __name__ == "__main__":
    print(file_dictionary.keys())
    print(hash_tree(create_tree()))