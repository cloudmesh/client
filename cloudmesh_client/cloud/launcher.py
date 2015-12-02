from __future__ import print_function
import subprocess
import platform

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

    def run(self, **kwargs):

        script = kwargs["script"]
        output = subprocess.check_output("script", shell=True)

        return output


def Launcher(kind):

        if kind.lower() in ["sh", "shell"]:
            return LauncherShell()
        else:
            ValueError("not yet implemented")
            return "not yet implemented"


