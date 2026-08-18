import argparse
from add import darwin_add
from init import darwin_init

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
