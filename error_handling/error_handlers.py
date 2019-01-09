import sys

import requests

from error_handling.error_codes import ErrorCodes


def is_error_response(response: requests.Response):
    return response.status_code >= 400


def print_response_error(response: requests.Response):
    try:
        json_dict = response.json()
        error_code = json_dict['error_code']
        message = json_dict['message']

        error_code_label = ErrorCodes(error_code).name

        print(f'Error {error_code_label} = {error_code}. "{message}"',file=sys.stderr)
    except:
        print(f'Unable to parse response "{response.text}"',file=sys.stderr)