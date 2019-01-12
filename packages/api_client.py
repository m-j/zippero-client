from typing import BinaryIO
from urllib.parse import urljoin

import requests

from error_handling.error_handlers import is_error_response, throw_response_error
from utils.constants import api_key_header


class ApiClient:
    repository_url: str
    api_key: str

    def __init__(self, repository_url: str, api_key: str):
        self.api_key = api_key
        self.repository_url = repository_url


    def post_package(self, file: BinaryIO):
        headers = {}

        if self.api_key is not None:
            headers[api_key_header] = self.api_key

        packages_url = urljoin(self.repository_url, 'packages')
        response = requests.post(packages_url, headers=headers, data=file)

        if is_error_response(response):
            throw_response_error(response)