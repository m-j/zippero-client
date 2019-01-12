from os import getcwd
from pathlib import Path

def version_check_command(args):
    name = args.name
    directory = args.directory

    package_directory = Path(getcwd()) / directory

       
