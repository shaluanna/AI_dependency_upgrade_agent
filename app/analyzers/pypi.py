import requests

from app.core.models import Dependency, PackageInfo


PYPI_URL = "https://pypi.org/pypi/{}/json"


def get_package_info(dependency: Dependency) -> PackageInfo:
    url = PYPI_URL.format(dependency.name)

    try:
        response = requests.get(
            url,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()
        latest_version = data["info"]["version"]

        update_available = False

        if dependency.current_version:
            update_available = (
                dependency.current_version != latest_version
            )

        return PackageInfo(
            name=dependency.name,
            current_version=dependency.current_version,
            latest_version=latest_version,
            update_available=update_available
        )

    except Exception as exc:
        return PackageInfo(
            name=dependency.name,
            current_version=dependency.current_version,
            latest_version=None,
            update_available=False,
            error=str(exc)
        )


def check_dependencies(dependencies):
    results = []

    for dependency in dependencies:
        result = get_package_info(dependency)
        results.append(result)

    return results