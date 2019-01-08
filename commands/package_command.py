import os

import shutil
import sys
from os import path

from utils.args_utils import get_directory_or_cwd
from utils.paths import zpspec_name
from utils.zpspec_utils import load_zpspec, fullname


def package_command(args):
    print('package command')

    directory = get_directory_or_cwd(args)

    zpspec_dict = load_zpsec_or_handle_err(directory)

    if zpspec_dict is None:
        return

    name = zpspec_dict['packageName']
    version = zpspec_dict['version']

    archive_path = path.join(directory, fullname(name, version) + '.zip')

    shutil.make_archive(archive_path, 'zip', directory)


def load_zpsec_or_handle_err(directory):
    zpspec_path = path.join(directory, zpspec_name)
    try:
        return load_zpspec(zpspec_path)
    except OSError as ex:
        print(f'Cannot read {zpspec_path}', file=sys.stderr)
        raise
        return None
