from src.database import Package, PackageHistory
from src.pypi_actions import package_pypi


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
