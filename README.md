# npm dependency server

A web server that provides a basic HTTP api for querying the dependency
tree of a [npm](https://npmjs.org) package.

## Prerequisites

* [Python 3.11](https://www.python.org/downloads/release/python-3116/)

## Getting Started

To install dependencies and start the server in development mode:

```sh
poetry install
poetry run ./manage.py runserver
```

The server will now be running on an available port (defaulting to 8000) and
will restart on changes to the src files.

Then we can try the `/package` endpoint. Here is an example that uses `curl` and
`jq`, but feel free to use any client.

```sh
curl -s http://localhost:8000/package/react/16.13.0 | jq .
```

Most of the code is boilerplate; the logic for the `/package` endpoint can be
found in [src/package.py](src/package.py), and some basic tests in
[test/test_package.py](test/test_package.py)

You can run the tests with:

```sh
poetry run pytest
```

The code is linted using `pre-commit`, you can run this via:

```sh
pre-commit
```

## Review

Should be fixed:
- PR has conflicts
- 2nd function `request_package()` is not used anywhere (might be useful if implementing async)
- Function & variable naming could be improved: e.g. `get_package()` -> `get_package_dependency_tree()`; `range` -> `version_range`
- Documentation: missing docstrings
- Get package should return the latest satisfying version: currently it returns the oldest satisfying version 
- If package does not have a description, the code fails (e.g. `snyk-docker-plugin`). 
    - Currently package description is also not returned to user
    - So either delete the description field or make it optional 
- Circular dependency: Dependency A -> Dependency B -> Dependency A will result in infinite recursion
    - Keep track of packages & versions already visited 
- Implement error handling for request to NPM and common errors (no matching package / version found)
- Fix the test & increase coverage


Tests:
- The 1 test does not pass (wrong versions of the dependencies)
- Should add more API tests for:
    - Testing getting a package with version range (e.g. "^10.1", "<2.1")
    - Test getting a package with no dependencies
    - Test edge cases:
        - Package version not specified - should return the latest version
        - Package does not exist - should return 404 (Not Found)
        - Package version out of range (e.g. -1) - should return 404 (Not Found)
        - Package is null 

Improvements:
- Could consider adding a cache to retrieve frequently requested packages faster (e.g. express)
- Could make the get_package() function asynchronous to speed up the dependency fetching 


