import requests
import semver

from packages.models import VersionedPackage

NPM_REGISTRY_URL = "https://registry.npmjs.org"


# REVIEW: use a more descriptive name e.g. get_package_dependency_tree(); range -> version_range
def get_package(name: str, range: str, visited_nodes: set = None) -> VersionedPackage:

    if visited_nodes is None:
        visited_nodes = set()

    # Fix for circular dependencies
    node_name = f"{name}/{range}"
    if node_name in visited_nodes:
        return VersionedPackage(
            name=name,
            version=range,
            description="",
        )

    # REVIEW: add function docstring
    url = f"{NPM_REGISTRY_URL}/{name}"

    # REVIEW: add error handling
    npm_package = requests.get(url).json()
    versions = list(npm_package["versions"].keys())
    # REVIEW: this returns the oldest satisfying version. Should be latest that matches
    version = semver.max_satisfying(versions, range)
    # REVIEW: add error handling in case matching version is not found
    if version not in npm_package["versions"]:
        return VersionedPackage(
            name=name,
            version=range,
            description="",
        )

    version_record = npm_package["versions"][version]

    package = VersionedPackage(
        name=version_record["name"],
        version=version_record["version"],
        # REVIEW: if package does not have description this fails. Make it optional just like with dependencies
        description=version_record.get("description", ""),
    )
    dependencies = version_record.get("dependencies", {})
    visited_nodes.add(node_name)

    # REVIEW: this could result in infinite recursion if there is depA -> depB -> depA loop.
    # Suggestion: keep track of nodes visited
    package.dependencies = [
        get_package(name=dep_name, range=dep_range, visited_nodes=visited_nodes)
        for dep_name, dep_range in dependencies.items()
    ]

    return package


# REVIEW: function not used anywhere
def request_package(name: str, range: str) -> tuple[VersionedPackage, dict]:
    # REVIEW: add function docstring
    url = f"{NPM_REGISTRY_URL}/{name}"

    npm_package = requests.get(url).json()

    versions = list(npm_package["versions"].keys())
    version = semver.min_satisfying(versions, range)
    version_record = npm_package["versions"][version]

    return VersionedPackage(
        name=version_record["name"],
        version=version_record["version"],
        description=version_record["description"],
    ), version_record.get("dependencies", {})
