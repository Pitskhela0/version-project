import re
from functools import total_ordering


@total_ordering
class Version:
    version_regex = (
        r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
        r"(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)"
        r"(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?"
        r"(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$"
    )

    @staticmethod
    def extract_version_components(version):
        if not isinstance(version, str):
            raise ValueError("Version type is not a string")

        matching = re.match(Version.version_regex, version)
        if not matching:
            raise ValueError("Version does not have valid format")

        major, minor, patch, pre_release, build = matching.groups()

        return {
            "major": int(major),
            "minor": int(minor),
            "patch": int(patch),
            "pre_release": pre_release,
            "build": build
        }

    def __init__(self, version):
        values = Version.extract_version_components(version)
        self.major = values["major"]
        self.minor = values["minor"]
        self.patch = values["patch"]
        self.pre_release = values["pre_release"]
        self.build = values["build"]

    @staticmethod
    def lt_pre_release(v1, v2):
        self_pre_release_list = v1.pre_release.split(".")
        other_pre_release_list = v2.pre_release.split(".")

        min_length = min(len(self_pre_release_list), len(other_pre_release_list))

        for i in range(min_length):
            self_part = self_pre_release_list[i]
            other_part = other_pre_release_list[i]

            if self_part.isdigit() and other_part.isdigit():
                if int(self_part) != int(other_part):
                    return int(self_part) < int(other_part)
            elif self_part.isdigit() and not other_part.isdigit():
                return True
            elif not self_part.isdigit() and other_part.isdigit():
                return False
            else:
                if self_part != other_part:
                    return self_part < other_part

        return len(self_pre_release_list) < len(other_pre_release_list)

    def __lt__(self, value):
        self_core = (self.major, self.minor, self.patch)
        other_core = (value.major, value.minor, value.patch)

        if self_core != other_core:
            return self_core < other_core

        if ((self.pre_release is None and value.pre_release is None) or
                (self.pre_release is None and value.pre_release is not None)):
            return False
        elif self.pre_release is not None and value.pre_release is None:
            return True
        else:
            return Version.lt_pre_release(self, value)

    def __eq__(self, value):
        return (self.major == value.major and
                self.minor == value.minor and
                self.patch == value.patch and
                self.pre_release == value.pre_release)

    def __str__(self):
        return (f"Version: {self.major}.{self.minor}.{self.patch}"
                f"{'-' + self.pre_release if self.pre_release else ''}"
                f"{'+' + self.build if self.build else ''}")
