import pytest
from src.version_project.version import Version

def test_equality():
    assert Version("1.2.3") == Version("1.2.3")
    assert Version("1.2.3-alpha") == Version("1.2.3-alpha")
    assert Version("1.2.3+build123") == Version("1.2.3+build123")

def test_inequality():
    assert Version("1.2.3") != Version("1.2.4")
    assert Version("1.2.3-alpha") != Version("1.2.3-beta")

def test_lt_basic():
    assert Version("1.2.3") < Version("1.2.4")
    assert Version("1.2.3") < Version("2.0.0")

def test_gt_basic():
    assert Version("2.1.0") > Version("2.0.5")
    assert Version("1.3.0") > Version("1.2.999")

def test_lt_prerelease_vs_release():
    assert Version("1.0.0-alpha") < Version("1.0.0")

def test_lt_prerelease_comparison():
    assert Version("1.0.0-alpha") < Version("1.0.0-beta")
    assert Version("1.0.0-alpha.1") < Version("1.0.0-alpha.beta")
    assert Version("1.0.0-beta.2") < Version("1.0.0-beta.11")

def test_str_representation():
    v = Version("1.2.3-alpha+build123")
    assert str(v) == "Version: 1.2.3-alpha+build123"