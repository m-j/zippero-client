from distutils.version import LooseVersion
from typing import Dict

from error_handling.exceptions import ZipperoClientException


def get_newest_package_from_package_info(package_info: Dict):
    versions = package_info['data']['versions'].copy()

    if len(versions) == 0:
        raise ZipperoClientException(f'No versions of {zpspec_name} found')

    versions.sort(key=LooseVersion)

    newest_version = versions[-1]
    return newest_version