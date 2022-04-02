import json
from distutils.version import LooseVersion
from os import getcwd
from pathlib import Path

from commands.publish_command import get_api_key
from error_handling.exceptions import ZipperoClientException
from packages.api_client import ApiClient
from packages.package_utils import get_newest_package_from_package_info
from utils.args_utils import get_directory_or_cwd
from utils.constants import zpspec_file_name
from utils.zpspec_utils import load_zpspec

def common_format(s: str):
    return s.strip().lower()


def package_version_command(args):
    package = args.package
    print(f'checking latest version for package {package}')

    repository = args.repository

    api_key = get_api_key(args)
    api_client = ApiClient(repository, api_key)

    response_json = api_client.get_package_info(package)

    newest_version = get_newest_package_from_package_info(response_json)

    print(common_format(newest_version))
