import os
import sys

def get_directory_or_cwd(args):
    if args.directory:
        return os.path.join(os.getcwd(), args.directory)
    else:
        return os.getcwd()
