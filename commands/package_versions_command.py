from commands.publish_command import get_api_key
from packages.api_client import ApiClient
from packages.package_utils import get_package_versions

def common_format(s: str):
    return s.strip().lower()


def package_versions_command(args):
    package = args.package

    repository = args.repository

    api_key = get_api_key(args)
    api_client = ApiClient(repository, api_key)

    response_json = api_client.get_package_info(package)

    versions = get_package_versions(response_json)

    for version in versions:
        print(version)
