import re  # regular expression engine, to check version validity


class Version:
    # take from: https://semver.org/  (press ctrl + link to go to website, and scroll to the bottom)
    version_regex = r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$"

    @staticmethod
    def unpack_version_elegant(version):
        # check type of argument for unexpected errors
        if not isinstance(version, str):
            raise Exception("Version type is not a string")

        matching = re.match(Version.version_regex, version)
        # check if version has valid format using regex
        if not matching:
            raise Exception("Version does not have valid format")

        # unpack using groups()
        major, minor, patch, pre_release, build = matching.groups()

        return {
            "major": int(major),
            "minor": int(minor),
            "patch": int(patch),
            "pre_release": pre_release,
            "build": build
        }

    def __init__(self, version):
        values = Version.unpack_version_elegant(version)
        # unpack and assign values
        self.major = values.get("major")
        self.minor = values.get("minor")
        self.patch = values.get("patch")
        self.pre_release = values.get("pre_release")
        self.build = values.get("build")

    # less than for pre_release
    @staticmethod
    def lt_pre_release(v1, v2):
        self_pre_release = v1.pre_release

        self_pre_release_list = v1.pre_release.split(".")
        other_pre_release_list = v2.pre_release.split(".")

        min_length = min(len(self_pre_release_list), len(other_pre_release_list))

        for i in range(min_length):
            self_part = self_pre_release_list[i]
            other_part = other_pre_release_list[i]

            # if both are numeric check numerically
            if self_part.isdigit() and other_part.isdigit():
                if int(self_part) != int(other_part):
                    return int(self_part) < int(other_part)
            elif self_part.isdigit() and not other_part.isdigit():
                return True
            elif not self_part.isdigit() and other_part.isdigit():
                return False
            # both are non-numerical
            else:
                if self_part != other_part:
                    return self_part < other_part

        # if result is not returned until check the sizes
        return len(self_pre_release_list) < len(other_pre_release_list)

    # less than
    def __lt__(self, value):
        self_core = (self.major, self.minor, self.patch)
        other_core = (value.major, value.minor, value.patch)

        if self_core != other_core:
            return self_core < other_core

        # if they are equal then check pre_release if it is present

        # equal because pre-release are both None or other one is pre_release and sel is not
        if (self.pre_release is None and value.pre_release is None) or (
                self.pre_release is None and value.pre_release is not None):
            return False
        # self is pre_release, so other one wins
        elif self.pre_release is not None and value.pre_release is None:
            return True
        else:
            return Version.lt_pre_release(self, value)

    # equality check
    def __eq__(self, value):
        return self.major == value.major and self.minor == value.minor and self.patch == value.patch and self.pre_release == value.pre_release

    # not equal
    def __ne__(self, value):
        return not self.__eq__(value)

    # greater than
    def __gt__(self, value):
        # if self does not equal to value and is not less than value -> then it is greater
        if self.__ne__(value) and not self.__lt__(value):
            return True
        else:
            return False

    # beautiful representation
    def __str__(self):
        return (f"Version: {self.major}.{self.minor}.{self.patch}"
                f"{'-' + self.pre_release if self.pre_release else ''}"
                f"{'+' + self.build if self.build else ''}"
                )


# def main():
#     to_test = [
#         ("1.0.0", "2.0.0"),
#         ("1.0.0", "1.42.0"),
#         ("1.2.0", "1.2.42"),
#         ("1.1.0-alpha", "1.2.0-alpha.1"),
#         ("1.0.1b", "1.0.10-alpha.beta"),
#         ("1.0.0-rc.1", "1.0.0"),
#     ]
#
#     for left, right in to_test:
#         assert Version(left) < Version(right), "le failed"
#         assert Version(right) > Version(left), "ge failed"
#         assert Version(right) != Version(left), "neq failed"
#         # assert Version(right) == Version(left), "eq failed"


# def main():
#     v = Version("1.1.1")
#     print(v)


# if __name__ == "__main__":
#     main()
