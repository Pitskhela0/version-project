# Semantic Version Comparator

This Python module provides a scaffold for implementing semantic version comparison,  
following the [Semantic Versioning](https://semver.org/) specification.

---

## Example Usage

The `Version` class is designed to support semantic comparisons using standard operators:

```python
Version("1.1.3") < Version("2.2.3")      # True
Version("1.3.0") > Version("0.3.0")      # True
Version("0.3.0b") < Version("1.2.42")    # True
Version("1.3.42") == Version("42.3.1")   # False
```

skeletoon
```python
class Version:
    def __init__(self, version):
        pass
```


test cases
```python
def main():
    to_test = [
        ("1.0.0", "2.0.0"),
        ("1.0.0", "1.42.0"),
        ("1.2.0", "1.2.42"),
        ("1.1.0-alpha", "1.2.0-alpha.1"),
        ("1.0.1b", "1.0.10-alpha.beta"),
        ("1.0.0-rc.1", "1.0.0"),
    ]

    for left, right in to_test:
        assert Version(left) < Version(right), "le failed"
        assert Version(right) > Version(left), "ge failed"
        assert Version(right) != Version(left), "neq failed"
```