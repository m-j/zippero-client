import re
from distutils.version import LooseVersion
from os import getcwd

from commands.publish_command import get_api_key
from error_handling.exceptions import ZipperoClientException
from packages.api_client import ApiClient
from packages.local_cache import LocalCache
from packages.package_installer import PackageInstaller
from packages.package_utils import get_newest_package_from_package_info
from utils.args_utils import get_directory_or_cwd
from utils.zpspec_utils import fullname

package_version_regex = r'(?P<name>[^@]+)@(?P<version>(0|[1-9]\d*)\.(0|[1-9]\d*)\.([0-9]\d*)(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?)'


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

    newest_version = get_newest_package_from_package_info(response_json)

    install_exact_version(requested_name, newest_version, target_path, package_installer)


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

    target_path = get_directory_or_cwd(args)

    if requested_version:
        install_exact_version(requested_name, requested_version, target_path, package_installer)
    else:
        install_newest_version(requested_name, target_path, package_installer, api_client)
