"""Test module for Version class"""

import pytest
from src.version_project.version import Version


class TestVersionParsing:
    """version string parsing and validation"""

    def test_valid_full_version(self):
        """parsing complete version with pre-release and build"""

        v = Version("2.1.3-rc.1+build.456")
        assert v.major == 2
        assert v.minor == 1
        assert v.patch == 3
        assert v.pre_release == "rc.1"
        assert v.build == "build.456"

    def test_invalid_version_strings(self):
        """invalid version strings -> raise exceptions"""

        invalid_versions = [
            "1.2.3.4",
            "01.2.3",
            "1.2.3-",
            "1.2.3+",
            "",
            "1.2.3-alpha..1",
        ]

        for invalid in invalid_versions:
            with pytest.raises(Exception):
                Version(invalid)


class TestVersionEquality:
    """version equality comparisons"""

    def test_equal_basic_versions(self):
        """equality of basic versions"""

        assert Version("1.2.3") == Version("1.2.3")
        assert Version("10.20.30") == Version("10.20.30")

    def test_equal_pre_release_versions(self):
        """equality of pre-release versions"""

        assert Version("1.2.3-alpha") == Version("1.2.3-alpha")
        assert Version("2.0.0-rc.1.2.3") == Version("2.0.0-rc.1.2.3")

    def test_not_equal_versions(self):
        """inequality of different versions"""

        assert Version("1.2.3") != Version("1.2.4")
        assert Version("1.2.3-alpha") != Version("1.2.3-beta")


class TestVersionComparison:
    """version comparison operations"""

    def test_version_comparison(self):
        """comparison based on core contents"""

        # comparison based on major
        assert Version("1.0.0") < Version("2.0.0")
        # comparison based on minor
        assert Version("1.1.0") < Version("1.2.0")
        # comparison based on patch
        assert Version("1.2.10") > Version("1.2.9")

    def test_pre_release_vs_release(self):
        """test pre-release versions are less than release versions"""

        assert Version("1.0.0-beta") < Version("1.0.0")
        assert Version("2.0.0-alpha") < Version("2.0.0")

    def test_pre_release_alphabetical_comparison(self):
        """alphabetical comparison of pre-release identifiers"""

        assert Version("1.0.0-alpha") < Version("1.0.0-beta")
        assert Version("1.0.0-beta") < Version("1.0.0-gamma")

    def test_pre_release_numeric_comparison(self):
        """numeric comparison of pre-release identifiers"""

        assert Version("1.0.0-alpha.1") < Version("1.0.0-alpha.2")
        assert Version("1.0.0-rc.1") < Version("1.0.0-rc.10")

    def test_pre_release_mixed_comparison(self):
        """mixed numeric/alphabetic pre-release comparison"""

        assert Version("1.0.0-alpha.1") < Version("1.0.0-alpha.beta")
        assert Version("1.0.0-1") < Version("1.0.0-alpha")

    def test_pre_release_length_comparison(self):
        """test if longer pre-release identifiers win when prefixes are equal"""

        assert Version("1.0.0-alpha") < Version("1.0.0-alpha.1")
        assert Version("1.0.0-alpha.1") < Version("1.0.0-alpha.1.beta")

    def test_semver_example_ordering(self):
        """the exact ordering example from SemVer specification"""

        versions = [
            "1.0.0-alpha",
            "1.0.0-alpha.1",
            "1.0.0-alpha.beta",
            "1.0.0-beta",
            "1.0.0-beta.2",
            "1.0.0-beta.11",
            "1.0.0-rc.1",
            "1.0.0",
        ]
        for i, v1 in enumerate(versions):
            for v2 in versions[i + 1 :]:
                assert Version(v1) < Version(v2), f"{v1} should be < {v2}"


class TestVersionStringRepresentation:
    """string representation of versions"""

    def test_basic_version_string(self):
        """string representation of basic versions"""

        v = Version("1.2.3")
        assert str(v) == "Version: 1.2.3"

    def test_full_version_string(self):
        """string representation of complete versions"""

        v = Version("1.2.3-rc.1+build.456")
        assert str(v) == "Version: 1.2.3-rc.1+build.456"


class TestEdgeCases:
    """edge cases and boundary conditions"""

    def test_zero_versions(self):
        """versions with zero components"""

        assert Version("0.0.0") == Version("0.0.0")
        assert Version("0.0.1") > Version("0.0.0")

    def test_complex_pre_release_identifiers(self):
        """complex pre-release identifier pattern"""

        assert Version("1.0.0-x.7.z.92") < Version("1.0.0-x.7.z.93")
        assert Version("1.0.0-alpha-beta") > Version("1.0.0-alpha.beta")

    def test_build_metadata_variations(self):
        """various build metadata patterns"""

        v1 = Version("1.0.0+20130313144700")
        v2 = Version("1.0.0+exp.sha.5114f85")
        v3 = Version("1.0.0+21AF26D3-117B344092BD")

        assert v1 == v2 == v3
