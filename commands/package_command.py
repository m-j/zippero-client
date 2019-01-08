import sys
import zipfile
from os import path, walk

import shutil

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

    walk_iterator = walk(directory)

    with zipfile.ZipFile(archive_path, 'w') as zip_file:
        for root, dirs, files in walk_iterator:
            for file in files:
                src_file_path = path.join(root, file)

                if path.samefile(src_file_path, archive_path):
                    continue

                zip_file.write(src_file_path, arcname=path.relpath(src_file_path, directory))


def load_zpsec_or_handle_err(directory):
    zpspec_path = path.join(directory, zpspec_name)
    try:
        return load_zpspec(zpspec_path)
    except OSError as ex:
        print(f'Cannot read {zpspec_path}', file=sys.stderr)
        raise
        return None
