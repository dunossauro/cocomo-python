from json import dumps
from pathlib import Path

from playhouse.shortcuts import model_to_dict

from .cocomo import sloccount as scc
from .database import LastPackage, Package, PackageHistory
from .history import full_info
from .package import unzip_package
from .pypi_actions import (
    download_file,
    download_last_package_version,
    package_basic_info,
    package_versions,
)
from .utils import json_parse, temp_path


def json(file, verbose=False, salary=110_140):
    for group, packages in json_parse(file):
        with temp_path('v3'):
            for package in packages:
                pkg = Package().select().where(Package.name == package).first()
                if not pkg:
                    pkg = Package(**package_basic_info(package))
                    pkg.save()

                last_version = package_versions(package, only_last=True)

                last = (
                    LastPackage()
                    .select()
                    .join(Package)
                    .where(
                        Package.name == package,
                        LastPackage.version == last_version,
                    )
                    .first()
                )

                if not last:
                    packge_path, last_version = download_last_package_version(
                        package
                    )

                    path = unzip_package(packge_path, 'vendor/', package)
                    cocomo = scc('vendor/' + path, salary=salary)

                    result = {
                        'version': last_version,
                        'group': group,
                    } | cocomo

                    LastPackage(name=pkg, **result).save()
                if verbose:
                    print(
                        dumps(
                            model_to_dict(
                                LastPackage()
                                .select()
                                .join(Package)
                                .where(
                                    Package.name == package,
                                    LastPackage.version == last_version,
                                )
                                .first()
                            )
                        )
                    )


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
                unzip_path = unzip_package(
                    local_file, Path('vendor'), package_name
                )
                df = scc(f'vendor/{unzip_path}', salary=salary)

                p.downloaded = True
                p.total_lines = df["total_lines"]
                p.total_cost = df["total_cost"]

                p.packge_type = 'wheel' if 'whl' in p.package_url else 'tar'

                p.save()

            except Exception as e:
                print(e)
                ...
