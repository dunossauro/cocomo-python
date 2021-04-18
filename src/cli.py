from json import dumps

from playhouse.shortcuts import model_to_dict

from .cocomo import sloccount as scc
from .database import LastPackage, Package
from .package import unzip_package
from .pypi_actions import (
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

                    path = unzip_package(packge_path, 'vendor/')
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
