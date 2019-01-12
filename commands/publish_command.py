from urllib.parse import urljoin

import requests
import os

from error_handling.error_handlers import is_error_response, throw_response_error
from packages.api_client import ApiClient
from utils.constants import api_key_header, api_key_environment_variable


def get_api_key(args):
    if args.key is not None:
        return args.key
    elif api_key_environment_variable in os.environ:
        return os.environ[api_key_environment_variable]
    else:
        return None


def publish_command(args):
    print('publish command')
    print(args)

    repository = args.repository
    file_path = args.file
    api_key = get_api_key(args)

    api_client = ApiClient(repository, api_key)

    with open(file_path, 'rb') as file:
        api_client.post_package(file)

    print(f'Package {file_path} published')