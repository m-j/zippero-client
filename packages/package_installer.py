import shutil

from packages.local_cache import LocalCache


class PackageInstaller:
    cache: LocalCache

    def __init__(self, cache: LocalCache, repository: str, api_key: str):
        self.api_key = api_key
        self.repository = repository
        self.cache = cache

    def install(self, requested_name: str, requested_version: str, target_path: str):
        self.cache.download_package_if_needed(requested_name, requested_version)
        source_path = self.cache.get_cache_path(requested_name, requested_version)

        shutil.unpack_archive(source_path, target_path)