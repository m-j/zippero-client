import sys
from distutils.version import StrictVersion
from os import getcwd
from urllib.parse import urljoin

import requests
import re

from error_handling.exceptions import ZipperoClientException
from packages.local_cache import LocalCache
from commands.publish_command import get_api_key
from error_handling.error_handlers import is_error_response, throw_response_error
from packages.package_installer import PackageInstaller
from utils.constants import api_key_header
from utils.zpspec_utils import fullname

package_version_regex = r'(?P<name>[^@]+)@(?P<version>[\d\.]+)'

#todo: extract api client to couple request and credentials

def try_extract_version(package: str):
    match = re.match(package_version_regex, package)
    if match:
        gd = match.groupdict()
        return (gd['name'], gd['version'])
    else:
        return None


def install_exact_version(requested_name, requested_version, target_path, package_installer: PackageInstaller):
    package_installer.install(requested_name, requested_version, target_path)
    print(f'Package {fullname(requested_name, requested_version)} installed under {target_path}')


def install_newest_version(requested_name, target_path, package_installer, repository, api_key):
    headers = {}

    if api_key is not None:
        headers[api_key_header] = api_key

    package_info_url = urljoin(repository, f'package-info/{requested_name}')

    info_response = requests.get(package_info_url, headers= headers)

    if is_error_response(info_response):
        throw_response_error(info_response)

    response_json = info_response.json()
    versions = response_json['data']['versions']

    if len(versions) == 0:
        raise ZipperoClientException(f'No versions of {requested_name} found')

    versions.sort(key=StrictVersion)

    requested_version = versions[-1]

    install_exact_version(requested_name, requested_version, target_path, package_installer)



def install_command(args):
    package = args.package
    print(f'installing package {package}')

    extracted = try_extract_version(package)
    repository = args.repository

    if extracted:
        (requested_name, requested_version) = extracted
    else:
        requested_name = package
        requested_version = None

    api_key = get_api_key(args)
    cache = LocalCache.create_from_user_directory(repository, api_key)
    package_installer = PackageInstaller(cache, repository, api_key)

    if 'directory' in args:
        target_path = args.directory
    else:
        target_path = getcwd()

    if requested_version:
        install_exact_version(requested_name, requested_version, target_path, package_installer)
    else:
        install_newest_version(requested_name, target_path, package_installer, repository, api_key)


