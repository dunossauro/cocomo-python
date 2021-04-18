from pathlib import Path

from src.cocomo import sloccount
from src.package import unzip_package
from src.utils import temp_path
from src.database import Package
from src.pypi_actions import package_pypi, download_file


def full_info(package_name, label=''):
    info = package_pypi(package_name)

    if not list(Package().select().where(Package.name == package_name)):
        for l in info['releases'].keys():
            if info["releases"][l]:
                pkg_data = dict(
                    name=package_name,
                    version=l,
                    license=info["info"]['license'],
                    url=info["info"]['project_url'],
                    downloaded=False,
                    total_lines=0,
                    total_cost=0,
                    date=info["releases"][l][0]['upload_time'],
                    package_name=info["releases"][l][0]['filename'],
                    package_url=info["releases"][l][0]['url'],
                    label=label,
                    packge_type='',
                )
                pkg = Package(**pkg_data)
                pkg.save()
    else:
        print('Package in database')


def package_history(package_name, label='', salary=110_140):
    full_info(package_name, label)
    with temp_path(package_name):
        for p in Package.select().where(
            Package.downloaded == False, Package.name == package_name
        ):
            try:
                local_file = download_file(p.package_url)
                unzip_path = unzip_package(local_file, Path('vendor'))
                df = sloccount(f'vendor/{unzip_path}', salary=salary)

                p.downloaded = True
                p.total_lines = df["total_lines"]
                p.total_cost = df["total_cost"]

                p.packge_type = 'wheel' if 'whl' in p.package_url else 'tar'

                p.save()

            except Exception:
                ...
