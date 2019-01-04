import requests

def install_command(args):
    package = args.package
    print(f'installing package {package}')

    with requests.Session() as session:
        response = session.get(f'http://localhost:7001/package-info/test.packageA', headers={'Zippero-Api-Key': 'xxx'})
        print(response.json())
