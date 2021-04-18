import tarfile
from collections import Counter
from pathlib import Path
from zipfile import ZipFile

from pkg_resources import Requirement
from pkginfo import SDist, Wheel


def unzip_package(wheel, output_path):
    if wheel.endswith('.whl') or wheel.endswith('.egg'):
        opener, mode, names = ZipFile, 'r', 'namelist'
    else:
        opener, mode, names = tarfile.open, 'r:gz', 'getnames'

    try:
        package = opener(wheel, mode)
        paths = Counter(
            [
                Path(x).parts[0]
                for x in getattr(package, names)()
                if 'dist-info' not in x  # six and psycopg2 case
            ]
        )
        package.extractall(output_path)
        package.close()
        return paths.most_common(1)[0][0]

    except Exception as e:
        print(e)
        ...


def package_dependencies(package_name, extra_packages=False):
    metadata = package_metadata(package_name)
    if extra_packages:
        packages = metadata.requires_dist
    else:
        packages = [
            package
            for package in metadata.requires_dist
            if "extra" not in package
        ]
    return [Requirement.parse(package).name for package in packages]


def package_metadata(pkgpath):
    if pkgpath.endswith('.tar.gz'):
        dist = SDist
    elif pkgpath.endswith('.whl'):
        dist = Wheel

    return dist(pkgpath)
