from httpx import get, stream


def download_file(url):
    local_filename = url.split('/')[-1]
    with stream('GET', url) as r:
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_bytes():
                f.write(chunk)
    return local_filename


def package_pypi(package_name):
    return get(
        f'https://pypi.org/pypi/{package_name}/json', timeout=None
    ).json()


def package_basic_info(package_name):
    info = package_pypi(package_name)

    return dict(
        name=package_name,
        license=info["info"]['license'],
        url=info["info"]['project_url'],
    )


def package_url(package_name, version):
    package_info = package_pypi(package_name)
    return package_info['releases'][version][0]["url"]


def package_versions(package_name, only_last=False):
    from distutils.version import StrictVersion

    package_info = package_pypi(package_name)
    versions = package_info['releases']
    sorted_versions = tuple(
        sorted(
            (
                version
                for version in versions
                if 'c' not in version
                and 'dev' not in version
                and len(version.split('.')) <= 3
                and len(version.split('.')) > 1
                and 'alpha' not in version
                and 'beta' not in version
                and '-b1' not in version
                and '-hg' not in version
                and not version.endswith('a')
                and not version.endswith('b')
                and not version.endswith('pre')
            ),
            key=StrictVersion,
            reverse=True,
        )
    )
    if only_last:
        return sorted_versions[0]
    return sorted_versions


def download_last_package_version(package_name):
    version = package_versions(package_name, True)
    return download_file(package_url(package_name, version)), version
