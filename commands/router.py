import argparse
import sys

from commands.prefetch_command import prefetch_command
from commands.init_command import init_command
from commands.install_command import install_command
from commands.package_command import package_command
from commands.publish_command import publish_command
from commands.version_check_command import version_check_command
from error_handling.exceptions import ZipperoClientException
from utils.constants import api_key_environment_variable
from commands.version_check_command import up_to_date_string, outdated_string


def configure_argparser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(title='subcommands', description='list of valid subcommands')

    install_parser = subparsers.add_parser('install', help='installs given package under given path. directory will be created if doesnt exist')
    install_parser.set_defaults(handler=install_command)
    install_parser.add_argument('package', type=str, help='name of package or name@version e.g. Package@1.0.1')
    install_parser.add_argument('--repository', '-r', type=str, required=True, help='repository url')
    install_parser.add_argument('--key', '-k', type=str, help=f'api key to use if not provided will use {api_key_environment_variable}')
    install_parser.add_argument('--directory', '-d', type=str, help='directory into which package will be installed. if not prowided cwd is used')

    package_parser = subparsers.add_parser('package', help='packages cwd containing zpspec.json file')
    package_parser.set_defaults(handler=package_command)
    package_parser.add_argument('--directory', '-d', type=str)

    publish_parser = subparsers.add_parser('publish', help=f'publishes package to this will read api key from {api_key_environment_variable} environment variable or from argument if provided')
    publish_parser.set_defaults(handler=publish_command)
    publish_parser.add_argument('file', type=str, help='path to zippero package file to publish')
    publish_parser.add_argument('--repository', '-r', type=str, help='url to target repository')
    publish_parser.add_argument('--key', '-k', type=str, help=f'api key to use if not provided will use {api_key_environment_variable}')

    init_parser = subparsers.add_parser('init', help='creates new zpspec file')
    init_parser.set_defaults(handler=init_command)
    init_parser.add_argument('--name', '-n', type=str, required=True, help='name of package')
    init_parser.add_argument('--version', '-v', type=str, required=True, help='version of package in format 1.0.0')
    init_parser.add_argument('--directory', '-d', type=str)

    version_check_parser = subparsers.add_parser('version-check', help=f'checks wheter installed package is up to date. returns either {up_to_date_string} or {outdated_string}. If zpspec is not present returns {outdated_string}.')
    version_check_parser.set_defaults(handler=version_check_command)
    version_check_parser.add_argument('--directory', '-d', type=str, required=False, help='directory where package is installed. if not provided cwd is used')
    version_check_parser.add_argument('--repository', '-r', type=str, help='url to target repository')
    version_check_parser.add_argument('--key', '-k', type=str, help=f'api key to use if not provided will use {api_key_environment_variable}')

    install_parser = subparsers.add_parser('prefetch', help='prefetches package to local cache')
    install_parser.set_defaults(handler=prefetch_command)
    install_parser.add_argument('package', type=str, help='name of package or name@version e.g. Package@1.0.1')
    install_parser.add_argument('--repository', '-r', type=str, required=True, help='repository url')
    install_parser.add_argument('--key', '-k', type=str, help=f'api key to use if not provided will use {api_key_environment_variable}')

    return parser


def route_commands():
    parser = configure_argparser()
    args = parser.parse_args()

    if 'handler' in args:
        try:
            args.handler(args)
        except ZipperoClientException as ex:
            print(ex.message, file=sys.stderr)
    else:
        parser.print_help()

