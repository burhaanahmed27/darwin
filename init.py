import os
import argparse

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

    print("Darwin repository initialised")

def main():
    parser = argparse.ArgumentParser() # object that can read arguments from command line
    subparsers = parser.add_subparsers(dest="command", required=True) # an object to register commands like init, add etc
        #required = True means subcommands are required
        #dest = "command" stores the command name in args.command

    init_parser = subparsers.add_parser('init', help = 'Create a local Git repository')
    init_parser.set_defaults(func=darwin_init) #associate the init command to the function

    args = parser.parse_args() #returns an object that contains the user's argument
    args.func(args) #the args.func attribute stores the associated method

if __name__ == "__main__":
    main()
