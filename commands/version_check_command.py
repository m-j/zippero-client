import json
from distutils.version import StrictVersion
from os import getcwd
from pathlib import Path

from commands.publish_command import get_api_key
from error_handling.exceptions import ZipperoClientException
from packages.api_client import ApiClient
from packages.package_utils import get_newest_package_from_package_info
from utils.args_utils import get_directory_or_cwd
from utils.constants import zpspec_file_name
from utils.zpspec_utils import load_zpspec

up_to_date_string = 'up_to_date'
outdated_string = 'outdated'


def common_format(s: str):
    return s.strip().lower()


def version_check_command(args):
    directory = get_directory_or_cwd(args)
    repository = args.repository

    api_key = get_api_key(args)

    api_client = ApiClient(repository, api_key)
    package_directory = Path(getcwd()) / directory
    zpspec_path = package_directory / zpspec_file_name

    try:
        json_dict = load_zpspec(str(zpspec_path))
    except:
        print(outdated_string)
        return

    zpspec_version = json_dict['version']
    zpspec_name = json_dict['packageName']

    response_json = api_client.get_package_info(zpspec_name)

    newest_version = get_newest_package_from_package_info(response_json)

    if common_format(zpspec_version) == common_format(newest_version):
        print(up_to_date_string)
    else:
        print(outdated_string)
