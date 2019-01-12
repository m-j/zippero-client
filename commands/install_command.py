import re
from distutils.version import StrictVersion
from os import getcwd

from commands.publish_command import get_api_key
from error_handling.exceptions import ZipperoClientException
from packages.api_client import ApiClient
from packages.local_cache import LocalCache
from packages.package_installer import PackageInstaller
from utils.zpspec_utils import fullname

package_version_regex = r'(?P<name>[^@]+)@(?P<version>[\d\.]+)'


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


def install_newest_version(requested_name, target_path, package_installer, api_client: ApiClient):
    response_json = api_client.get_package_info(requested_name)

    versions = response_json['data']['versions']

    if len(versions) == 0:
        raise ZipperoClientException(f'No versions of {requested_name} found')

    versions.sort(key=StrictVersion)

    requested_version = versions[-1]

    install_exact_version(requested_name, requested_version, target_path, package_installer)


def install_command(args):
    package = args.package
    print(f'installing package {package}')

    name_version_tuple = try_extract_version(package)
    repository = args.repository

    if name_version_tuple:
        (requested_name, requested_version) = name_version_tuple
    else:
        requested_name = package
        requested_version = None

    api_key = get_api_key(args)
    api_client = ApiClient(repository, api_key)
    cache = LocalCache.create_from_user_directory(api_client)
    package_installer = PackageInstaller(cache)

    if 'directory' in args:
        target_path = args.directory
    else:
        target_path = getcwd()

    if requested_version:
        install_exact_version(requested_name, requested_version, target_path, package_installer)
    else:
        install_newest_version(requested_name, target_path, package_installer, api_client)
