from .package import unzip_package
from .pypi_actions import download_last_package_version
from .cocomo import sloccount as scc
from .utils import temp_path, json_parse
from .database import LastPackage


def json(file, salary=110_140, verbose=False):
    out = []
    for group, packages in json_parse(file):
        with temp_path('v3'):
            for package in packages:
                packge_path, last_version = download_last_package_version(
                    package
                )
                path = unzip_package(packge_path, 'vendor/')
                cocomo = scc('vendor/' + path, salary=salary)
                result = {
                    'name': package,
                    'version': last_version,
                    'group': group,
                } | cocomo
                LastPackage(**result).save()
                out.append(result)
                if verbose:
                    print(result)
