from pathlib import Path
from typing import List, Optional
from urllib.parse import urljoin

import requests

from error_handling.exceptions import ZipperoClientException
from packages.api_client import ApiClient
from utils.constants import zippero_user_directory, api_key_header
from utils.zpspec_utils import fullname

cache_user_directory_name = 'cache'


class LocalCache:
    api_client: ApiClient
    zippero_user_directory: Path
    zippero_cache_directory: Path
    packages: List[str]

    def __init__(self, user_home: Path, api_client: ApiClient):
        self.api_client = api_client
        self.zippero_cache_directory = user_home.joinpath(zippero_user_directory)
        self.zippero_cache_directory = self.zippero_cache_directory.joinpath(cache_user_directory_name)

    def scan(self):
        if not self.zippero_cache_directory.exists():
            self.zippero_cache_directory.mkdir(parents=True)

        packages = [str(p.stem) for p in self.zippero_cache_directory.iterdir() if p.is_file()]
        self.packages = packages

    def download_package_if_needed(self, name: str, version: str):
        full = fullname(name, version)

        if full in self.packages:
            return

        print('Downloading package to cache...')

        response_chunks = self.api_client.get_package(name, version)

        try:
            target_file_path = self.get_cache_path(name, version)
            with open(target_file_path, 'wb') as file:
                for chunk in response_chunks:
                    file.write(chunk)
        except OSError:
            raise ZipperoClientException(f'Failed to write data to file {target_file_path}')

        print(f'Package stored under {target_file_path}')

    def get_cache_path(self, name: str, version: str):
        return str(self.zippero_cache_directory.joinpath(fullname(name, version) + '.zip'))

    @staticmethod
    def create_from_user_directory(api_client: ApiClient):
        cache = LocalCache(Path.home(), api_client)
        cache.scan()
        return cache

    def is_package_in_cache(self, name: str, version: str):
        return fullname(name, version) in self.packages
