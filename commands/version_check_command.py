import json
from distutils.version import StrictVersion
from os import getcwd
from pathlib import Path

from commands.publish_command import get_api_key
from error_handling.exceptions import ZipperoClientException
from packages.api_client import ApiClient
from utils.constants import zpspec_file_name
from utils.zpspec_utils import load_zpspec

up_to_date_string = 'up_to_date'
outdated_string = 'outdated'


def common_format(s: str):
    return s.strip().lower()


def version_check_command(args):
    name = args.name
    directory = args.directory
    repository = args.repository

    api_key = get_api_key(args)

    api_client = ApiClient(repository, api_key)
    package_directory = Path(getcwd()) / directory
    zpspec_path = package_directory / zpspec_file_name

    json_dict = load_zpspec(str(zpspec_path))
    zpspec_version = json_dict['version']
    zpspec_name = json_dict['packageName']

    response_json = api_client.get_package_info(name)

    versions = response_json['data']['versions']

    if len(versions) == 0:
        raise ZipperoClientException(f'No versions of {requested_name} found')

    versions.sort(key=StrictVersion)

    newest_version = versions[-1]

    if common_format(zpspec_name) == common_format(name) \
            and common_format(zpspec_version) == common_format(newest_version):
        print(up_to_date_string)
    else:
        print(outdated_string)
