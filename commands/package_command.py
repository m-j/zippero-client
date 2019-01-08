import shutil
import sys
from os import path

from utils.paths import zpspec_name
from utils.zpspec_utils import load_zpspec, fullname


def package_command(args):
    print('package command')
    print(args)

    directory = args.directory
    zpspec_path = path.join(directory, zpspec_name)

    zpspec_dict = load_zpsec_or_handle_err(zpspec_path)
    name = zpspec_dict['packageName']
    version = zpspec_dict['version']

    archive_path = path.join(directory, fullname(name, version) + '.zip')

    shutil.make_archive(archive_path, 'zip', directory)


def load_zpsec_or_handle_err(zpspec_path):
    try:
        return load_zpspec(zpspec_path)
    except OSError as ex:
        print(f'Directory {directory} does not contain {zpspec_name}', file=sys.stderr)
        raise
