import json
import os

from utils.args_utils import get_directory_or_cwd
from utils.constants import zpspec_file_name


def init_command(args):
    name = args.name
    version = args.version

    zpspec_json_dict = {
        'packageName': name,
        'version': version
    }

    directory = get_directory_or_cwd(args)

    zpspec_path = os.path.join(directory, zpspec_file_name)

    with open(zpspec_path, 'tx') as file:
        json.dump(zpspec_json_dict, file)

    print(f'Created zpspec file under {zpspec_path}')
