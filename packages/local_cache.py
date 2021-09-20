import os
from pathlib import Path
from typing import List
from os import listdir
from os.path import isfile, join
import re
from error_handling.exceptions import ZipperoClientException
from packages.api_client import ApiClient
from utils.constants import zippero_user_directory
from utils.zpspec_utils import fullname
from distutils.version import StrictVersion

cache_user_directory_name = 'cache'
package_name_version_match_regular_expression = '^([a-zA-Z0-9_., ]*)@([Z0-9_.]*)(.zip)$'
max_number_of_packages_versions = 5


class LocalCache:
    api_client: ApiClient
    zippero_user_directory: Path
    zippero_cache_directory: Path
    packages: List[str]

    def __init__(self, user_home: Path, api_client: ApiClient):
        self.api_client = api_client
        self.zippero_cache_directory = user_home.joinpath(zippero_user_directory)
        self.zippero_cache_directory = self.zippero_cache_directory.joinpath(cache_user_directory_name)

    def _build_packages_versions_dict(self):
        result = {}
        packages = [f for f in listdir(self.zippero_cache_directory) if isfile(join(self.zippero_cache_directory, f))]
        for file_name in packages:
            package_name = re.search(package_name_version_match_regular_expression, file_name).group(1)
            package_version = re.search(package_name_version_match_regular_expression, file_name).group(2)
            if package_name in result:
                result[package_name].append(package_version)
            else:
                result[package_name] = []
                result[package_name].append(package_version)
        return result

    def clean(self):
        packages_version = self._build_packages_versions_dict()
        for package in packages_version:
            versions = packages_version[package]
            versions.sort(key=StrictVersion)
            if len(versions) > max_number_of_packages_versions:
                end_idx = len(versions) - max_number_of_packages_versions
                for version in reversed(versions[0:end_idx]):
                    full_path = self.zippero_cache_directory.joinpath(f'{package}@{version}.zip')
                    print(f'Cleaning obsolete package from cache - {package}@{version}')
                    os.remove(full_path)

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

        print(f'Cleaning cache...')

        self.clean()

        print(f'Cleaning cache done!')

    def get_cache_path(self, name: str, version: str):
        return str(self.zippero_cache_directory.joinpath(fullname(name, version) + '.zip'))

    @staticmethod
    def create_from_user_directory(api_client: ApiClient):
        cache = LocalCache(Path.home(), api_client)
        cache.scan()
        return cache

    def is_package_in_cache(self, name: str, version: str):
        return fullname(name, version) in self.packages
