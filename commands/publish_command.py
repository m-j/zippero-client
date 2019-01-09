from urllib.parse import urljoin

import requests
import os

from error_handling.error_handlers import is_error_response, print_response_error
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

    file_path = args.file
    response = None

    with open(file_path, 'rb') as file:
        headers= {}

        api_key = get_api_key(args)
        if api_key is not None:
            headers[api_key_header] = api_key

        repository= args.repository

        packages_url = urljoin(repository, 'packages')

        response = requests.post(packages_url, headers=headers, data=file)

    if is_error_response(response):
        print_response_error(response)
    else:
        print(f'Package {file_path} published')
