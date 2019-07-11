from commands.install_command import try_extract_version
from commands.publish_command import get_api_key
from packages.api_client import ApiClient
from packages.local_cache import LocalCache
from packages.package_utils import get_newest_package_from_package_info


def prefetch_command(args):
    package = args.package

    print(f'prefetching package {package}')

    name_version_tuple = try_extract_version(package)
    repository = args.repository

    api_key = get_api_key(args)
    api_client = ApiClient(repository, api_key)
    cache = LocalCache.create_from_user_directory(api_client)

    if name_version_tuple:
        (requested_name, requested_version) = name_version_tuple
    else:
        requested_name = package

        response_json = api_client.get_package_info(requested_name)
        newest_version = get_newest_package_from_package_info(response_json)

        requested_version = newest_version

    cache.download_package_if_needed(requested_name, requested_version)