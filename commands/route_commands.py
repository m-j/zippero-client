import argparse

from commands.install_command import install_command
from commands.package_command import package_command
from commands.publish_command import publish_command


def configure_argparser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(title='subcommands', description='list of valid subcommands')

    install_parser = subparsers.add_parser('install')
    install_parser.set_defaults(handler=install_command)
    install_parser.add_argument('package', type=str, help='name of package or name@version e.g. Package@1.0.1')

    package_parser = subparsers.add_parser('package')
    package_parser.set_defaults(handler=package_command)

    publish_parser = subparsers.add_parser('publish')
    publish_parser.set_defaults(handler=publish_command)

    return parser


def route_commands():
    parser = configure_argparser()
    args = parser.parse_args()

    if 'handler' in args:
        args.handler(args)
    else:
        parser.print_help()

