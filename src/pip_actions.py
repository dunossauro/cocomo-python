from re import IGNORECASE, findall
from .utils import execute_command, format_regex_package_name
from .package import package_dependencies


def download_package_whell(package, deps=False):
    cmd = 'pip download {}'
    regex = r'/({}.*[\.whl|\.tar\.gz])[\s|\\n|#]?\(?\d?'

    if deps:
        out = execute_command(cmd.format(package))
    else:
        out = execute_command(cmd.format(f'--no-deps {package}'))

    package_name = min(
        findall(
            regex.format(format_regex_package_name(package)), out, IGNORECASE
        ),
        key=len,
    )

    package_info = {
        'name': package,
        'package_path': package_name,
    }
    if deps:
        return package_info | {
            'dependencies': package_dependencies(package_name),
        }
    return package_info


def download_packs(libs, deps=False):
    return [download_package_whell(lib, deps) for lib in libs]
