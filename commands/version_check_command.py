import json
from distutils.version import StrictVersion
from os import getcwd
from pathlib import Path

from commands.publish_command import get_api_key
from error_handling.exceptions import ZipperoClientException
from packages.api_client import ApiClient
from utils.constants import zpspec_file_name

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

    with open(str(zpspec_path), 'rt') as file:
        json_dict = json.load(file)
        zpspec_version = json_dict['version']
        zpspec_name = json_dict['packageName']

    response_json = api_client.get_package_info(name)

    versions = response_json['data']['versions']

    if len(versions) == 0:
        raise ZipperoClientException(f'No versions of {requested_name} found')

    versions.sort(key=StrictVersion)

    newest_version = versions[-1]

    # if common_format(zpspec_name) == common_format(name) \
    #     and common_format(zpspec_version) ==  common_format(r)



