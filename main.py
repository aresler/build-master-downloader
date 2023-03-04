import argparse
import configparser
import os
import requests
import shutil
from installer import install_app


class InvalidFilePatternError(Exception):
    def __init__(self, pattern):
        self.message = f"Invalid file pattern: {pattern}\nPlease make sure it includes {{build}} placeholder"
        super().__init__(self.message)


class TCclient:
    def __init__(self, config):
        self.base_url = self.validate_base_url(config['downloader']['base_url'])
        self.token = config['downloader']['token']
        self.verify = config.getboolean('downloader', 'ssl_verify')

    @staticmethod
    def validate_link(link: str) -> str:
        if not link.startswith('/'):
            link = '/' + link
        return link

    @staticmethod
    def validate_target_dir(target_dir: str) -> str:
        if not target_dir.endswith('/'):
            target_dir = target_dir + '/'
        return target_dir

    @staticmethod
    def validate_base_url(url: str) -> str:
        if url.endswith('/'):
            url = url[:-1]
        return url

    def get(self, method: str, params: dict = None):
        base_url = self.base_url
        token = self.token
        verify = self.verify

        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {token}'
        }

        method = self.validate_link(method)

        try:
            r = requests.get(url=base_url + method, headers=headers, params=params, verify=verify)
        except requests.exceptions.ConnectionError as e:
            raise e

        if r.status_code == 200:
            return r.json()
        else:
            print(r.text)
            exit(1)

    def download_file(self, link, file_name, target_dir):
        base_url = self.base_url
        token = self.token
        verify = self.verify

        headers = {
            'Authorization': f'Bearer {token}'
        }

        link = self.validate_link(link)
        target_dir = self.validate_target_dir(target_dir)

        print(
            f'File URL: {base_url + link}\n'
            f'Downloading file {file_name} to {target_dir}\n\n'
            f'Download is in progress, please wait until finished...'
        )
        with requests.get(base_url + link, stream=True, headers=headers, verify=verify) as r:
            with open(target_dir + file_name, 'wb') as f:
                shutil.copyfileobj(r.raw, f)

        if r.status_code == 200:
            print('Finished downloading.')


def validate_file_pattern(self):
    pattern = self.file_pattern
    if '{build}' not in pattern:
        raise InvalidFilePatternError(pattern)


def find_latest_build(builds) -> dict:
    # _list = builds['build']
    # latest = max(_list, key=lambda x: x['id'])
    latest = builds['build'][0]
    return latest


if __name__ == '__main__':
    project_dir = os.path.dirname(os.path.abspath(__file__))
    config = configparser.ConfigParser()
    config.read(project_dir + '/config.ini')

    parser = argparse.ArgumentParser()
    parser.add_argument("-b", "--build-type", type=str, required=True,
                        help="Built configuration ID")
    parser.add_argument("-f", "--file-pattern", type=str, required=True,
                        help="Artifact file pattern. E.g. pycharmPC-{build}-aarch64.dmg")
    parser.add_argument("-t", "--target-dir", default=os.getcwd(), type=str, required=False,
                        help="[OPTIONAL] Download directory. Default is current workdir")
    args = parser.parse_args()

    clnt = TCclient(config)

    build_type: str = args.build_type
    file_pattern: str = args.file_pattern
    target_dir: str = args.target_dir

    builds = clnt.get(
        method=f'/app/rest/buildTypes/id:{build_type}/builds/',
        params={'locator': 'branch:master,status:success,state:finished,count:1'}
        # count:1 should always get the latest build
    )

    build = find_latest_build(builds)
    build_id: int = build['id']
    build_number: str = build['number']

    file_name = file_pattern.replace('{build}', build_number)
    file_link = f'/app/rest/builds/id:{build_id}/artifacts/content/{file_name}'
    clnt.download_file(file_link, file_name, target_dir)

    choice = input('\nTry to install? y/n: ')

    if choice == 'y':
        install_dir = config['installer']['install_dir']
        install_app(f'{target_dir}/{file_name}', install_dir)
