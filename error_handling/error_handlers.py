import sys

import requests

from error_handling.error_codes import ErrorCodes
from error_handling.exceptions import ZipperoClientException


def is_error_response(response: requests.Response):
    return response.status_code >= 400


def throw_response_error(response: requests.Response):
    try:
        json_dict = response.json()
        error_code = json_dict['error_code']
        message = json_dict['message']

        error_code_label = ErrorCodes(error_code).name

        raise ZipperoClientException(f'Error {error_code_label} = {error_code}. "{message}"')
    except Exception as ex:
        if not issubclass(type(ex), ZipperoClientException):
            raise ZipperoClientException(f'Unable to parse response "{response.text}"')
        else:
            raise


def print_response_error_and_exit(response: requests.Response):
    throw_response_error(response)
    #todo: exit program and return exit code