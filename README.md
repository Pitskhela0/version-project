# Semantic Version Comparator

This Python module provides parsing and comparing semantic versions according to the Semantic Versioning specification.

---

## Overview

This library helps you handle version strings in your Python projects. Whether you're building a package manager, dependency resolver, or just need to compare software versions, this tool makes it simple and reliable.

## Features
- SemVer style comparison between versions
- Parse version strings like 1.2.3, 2.0.0-alpha, 1.0.0+build123
- Validate versions
- Support pre_release versions and metadata


## Installation
``git clone https://github.com/Pitskhela0/version-project.git``

``cd version-project``

``uv sync``

## Examples and operations

### supported operations
- <, >, ==, != - Version comparison
- str() - String representation

### ordering example
~~~
versions = [
    "1.0.0-alpha",
    "1.0.0-alpha.1", 
    "1.0.0-alpha.beta",
    "1.0.0-beta",
    "1.0.0-beta.2",
    "1.0.0-beta.11", 
    "1.0.0-rc.1",
    "1.0.0"
]

# ordering follows SemVer specification
for i in range(len(versions) - 1):
    assert Version(versions[i]) < Version(versions[i + 1])
    print(f"{versions[i]} < {versions[i + 1]}")
~~~
## Testing
~~~
uv run pytest
~~~

## Resources
SemVer 2.0.0:
https://semver.org/#backusnaur-form-grammar-for-valid-semver-versions