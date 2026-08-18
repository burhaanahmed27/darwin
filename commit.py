import hashlib
import json
import os

dict = {}

# loading the dictionary from index
with open(".darwin/index", "r") as f:
    file_dictionary = json.load(f)

class DirectoryNode:
    def __init__(self, file_name):
        self.file_name = file_name
        self.children = []

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
    for root, subFolder, files in os.walk("."):
        if not is_node_created(root): # if it doesn't have a node yet
            node = DirectoryNode(root) # create the node
            dict[root] = node # add it to the dictionary
        else: # if it does have a node
            node = dict[root] # just get it from the dictionary

        for s in subFolder: # for each of the subFolders
            child_node = DirectoryNode(s) # create the node
            node.add_child(child_node) # add it to the tree

            # adding the relative path to the dictionary's keys
            full_path = os.path.join(root, s)
            dict[full_path] = child_node

        for f in files:
            child_node = DirectoryNode(f)
            node.add_child(child_node)

            # adding the relative path to the dictionary's keys
            full_path = os.path.join(root, f)
            dict[full_path] = child_node

    return dict['.']

# encoding the tree to its hash
def hash_tree(tree):
    hash = hashlib.sha256()
    for child in tree.children:
        if child.children == []:
            full_path = os.path.join(tree, child.file_name)
            child_hash = file_dictionary[full_path]
        else:
            full_path = os.path.join(tree, child.file_name)
            child_hash = hash_tree(dict[full_path])

        concatenation = child.file_name + child_hash
        hash.update(concatenation.encode())

    return hash.hexdigest()

if __name__ == "__main__":
    hash_tree(create_tree())