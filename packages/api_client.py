from typing import BinaryIO, Dict, Optional
from urllib.parse import urljoin

import requests

from error_handling.error_handlers import is_error_response, throw_response_error
from error_handling.exceptions import ZipperoClientException
from utils.constants import api_key_header
download_chunk_size = 1024*1024


class ApiClient:
    repository_url: str
    api_key: str

    def __init__(self, repository_url: str, api_key: str):
        self.api_key = api_key
        self.repository_url = repository_url

    def _build_headers(self):
        headers = {}

        if self.api_key is not None:
            headers[api_key_header] = self.api_key

        return headers

    def post_package(self, file: BinaryIO):
        headers = self._build_headers()

        packages_url = urljoin(self.repository_url, 'packages')
        response = requests.post(packages_url, headers=headers, data=file)

        if is_error_response(response):
            throw_response_error(response)

    def get_package_info(self, name: str) -> Dict:
        headers = self._build_headers()

        package_info_url = urljoin(self.repository_url, f'package-info/{name}')

        info_response = requests.get(package_info_url, headers=headers)

        if is_error_response(info_response):
            throw_response_error(info_response)

        response_json = info_response.json()
        return response_json

    def get_package(self, name: str, version: str):
        headers = self._build_headers()

        package_url = urljoin(self.repository_url, f'packages/{name}/{version}')
        response = requests.get(package_url, headers= headers, stream=True)

        if is_error_response(response):
            throw_response_error(response)

        return response.iter_content(download_chunk_size)


