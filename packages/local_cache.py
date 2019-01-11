from pathlib import Path
from typing import List, Optional
from urllib.parse import urljoin

import requests

from error_handling.exceptions import ZipperoClientException
from utils.constants import zippero_user_directory, api_key_header
from utils.zpspec_utils import fullname

cache_user_directory_name = 'cache'
download_chunk_size = 1024*1024

class LocalCache:
    api_key: Optional[str]
    repository_url: str
    zippero_user_directory: Path
    zippero_cache_directory: Path
    packages: List[str]

    def __init__(self, user_home: Path, repository_url: str, api_key: Optional[str]):
        self.api_key = api_key
        self.repository_url = repository_url
        self.zippero_cache_directory = user_home.joinpath(zippero_user_directory)
        self.zippero_cache_directory = self.zippero_cache_directory.joinpath(cache_user_directory_name)

    def scan(self):
        if not self.zippero_cache_directory.exists():
            self.zippero_cache_directory.mkdir(parents=True)

        packages = [str(p) for p in self.zippero_cache_directory.iterdir() if p.is_file()]
        self.packages = packages

    def download_package_if_needed(self, name: str, version: str):
        headers = {}

        if self.api_key is not None:
            headers[api_key_header] = self.api_key

        package_url = urljoin(self.repository_url, f'packages/{name}/{version}')

        full = fullname(name, version)

        if full in self.packages:
            return

        response = requests.get(package_url, headers= headers, stream=True)

        print('Downloading package to cache...')

        try:
            target_file_path = self.get_cache_path(name, version)
            with open(target_file_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=download_chunk_size):
                    file.write(chunk)
        except:
            raise ZipperoClientException(f'Failed to download file {package_url} and save it in cache under {target_file_path}')

        print(f'Package stored under {target_file_path}')

    def get_cache_path(self, name: str, version: str):
        return str(self.zippero_cache_directory.joinpath(fullname(name, version) + '.zip'))

    @staticmethod
    def create_from_user_directory(repository: str, api_key: Optional[str]):
        cache = LocalCache(Path.home(), repository, api_key)
        cache.scan()
        return cache

    def is_package_in_cache(self, name: str, version: str):
        return fullname(name, version) in self.packages
