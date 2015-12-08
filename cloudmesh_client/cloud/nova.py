from __future__ import print_function


class Nova(object):
    # noinspection PyPep8Naming
    @classmethod
    def remove_subjectAltName_warning(cls, content):
        result = []
        for line in content.split("\n"):
            if "subjectAltName" in line:
                pass
            elif "SubjectAltNameWarning" in line:
                pass
            else:
                result.append(line)
        return "\n".join(result)
