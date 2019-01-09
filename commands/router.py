import argparse

from commands.init_command import init_command
from commands.install_command import install_command
from commands.package_command import package_command
from commands.publish_command import publish_command
from utils.constants import api_key_environment_variable


def configure_argparser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(title='subcommands', description='list of valid subcommands')

    install_parser = subparsers.add_parser('install')
    install_parser.set_defaults(handler=install_command)
    install_parser.add_argument('package', type=str, help='name of package or name@version e.g. Package@1.0.1')

    package_parser = subparsers.add_parser('package', help='packages cwd containing zpspec.json file')
    package_parser.set_defaults(handler=package_command)
    package_parser.add_argument('--directory', '-d', type=str)

    publish_parser = subparsers.add_parser('publish', help=f'publishes package to this will read api key from {api_key_environment_variable} environment variable or from argument if provided')
    publish_parser.set_defaults(handler=publish_command)
    publish_parser.add_argument('file', type=str, help='path to zippero package file to publish')
    publish_parser.add_argument('--repository', '-r', type=str, help='url to target repository')
    publish_parser.add_argument('--key', '-k', type=str, help=f'api key to use if not provided will use {api_key_environment_variable}')

    init_parser = subparsers.add_parser('init')
    init_parser.set_defaults(handler=init_command)
    init_parser.add_argument('--name', '-n', type=str, required=True, help='name of package')
    init_parser.add_argument('--version', '-v', type=str, required=True, help='version of package in format 1.0.0')
    init_parser.add_argument('--directory', '-d', type=str)

    return parser


def route_commands():
    parser = configure_argparser()
    args = parser.parse_args()

    if 'handler' in args:
        args.handler(args)
    else:
        parser.print_help()

