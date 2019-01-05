import json
import os

from utils.paths import zpspec_name


def init_command(args):
    name = args.name
    version = args.version

    zpspec_json_dict = {
        'packageName': name,
        'version': version
    }

    cwd = os.getcwd()
    zpspec_path = os.path.join(cwd, zpspec_name)

    with open(zpspec_path, 'tx') as file:
        json.dump(zpspec_json_dict, file)
