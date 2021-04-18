from pathlib import Path

from src.cocomo import sloccount
from src.package import unzip_package
from src.utils import temp_path
from src.database import Package, PackageHistory
from src.pypi_actions import package_pypi, download_file


def full_info(package_name, label=''):
    info = package_pypi(package_name)

    pkg = Package().select().where(Package.name == package_name).first()
    if not pkg:
        pkg = Package(
            name=package_name,
            license=info["info"]['license'],
            url=info["info"]['project_url'],
        )
        pkg.save()

    for release in info['releases'].keys():
        if info["releases"][release]:
            release_info = info["releases"][release][0]

            pkg_release = (
                PackageHistory()
                .select()
                .where(PackageHistory.version == release)
                .first()
            )

            if not pkg_release:
                pkg_history = PackageHistory(
                    name=pkg,
                    version=release,
                    date=release_info['upload_time'],
                    package_name=release_info['filename'],
                    package_url=release_info['url'],
                )

                pkg_history.save()


def package_history(package_name, label='', salary=110_140):
    full_info(package_name, label)
    with temp_path(package_name):
        for p in (
            PackageHistory.select()
            .join(Package)
            .where(
                PackageHistory.downloaded == False,
                Package.name == package_name,
            )
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
