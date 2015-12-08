from __future__ import print_function
import subprocess

from cloudmesh_client.cloud.ListResource import ListResource


class LauncherProvider(ListResource):
    def info(self, **kwargs):
        ValueError("not yet implemented")
        return "not yet implemented"

    def list(self, **kwargs):
        ValueError("not yet implemented")
        return "not yet implemented"

    def run(self, **kwargs):
        ValueError("not yet implemented")
        return "not yet implemented"

    def resume(self, **kwargs):
        ValueError("not yet implemented")
        return "not yet implemented"

    def suspend(self, **kwargs):
        ValueError("not yet implemented")
        return "not yet implemented"

    def kill(self, **kwargs):
        ValueError("not yet implemented")
        return "not yet implemented"

    def details(self, **kwargs):
        ValueError("not yet implemented")
        return "not yet implemented"

    def clear(self, **kwargs):
        ValueError("not yet implemented")
        return "not yet implemented"

    def refresh(self, **kwargs):
        ValueError("not yet implemented")
        return "not yet implemented"


class LauncherShell(LauncherProvider):
    def __init__(self):
        pass

    def run(self, **kwargs):
        script = kwargs["script"].strip("\n")

        print(">>>>", script)
        # output = Shell.sh(script)
        output = subprocess.check_output(script, shell=True)
        print("OOOOOO", output)

        return output


# noinspection PyPep8Naming
def Launcher(kind):
    if kind.lower() in ["sh", "shell"]:
        return LauncherShell()
    else:
        ValueError("not yet implemented")
        return "not yet implemented"
