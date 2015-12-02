from __future__ import print_function
import subprocess
import platform

from cloudmesh_client.cloud.ListResource import ListResource


class LauncherProvider(ListResource):

    def info(self, **kwargs):
        ValueError("not yet implemented")
        return "not yet implemente"

    def list(self, **kwargs):
        ValueError("not yet implemented")
        return "not yet implemente"

    def run(self, **kwargs):
        ValueError("not yet implemented")
        return "not yet implemente"

    def resume(self, **kwargs):
        ValueError("not yet implemented")
        return "not yet implemente"

    def suspend(self, **kwargs):
        ValueError("not yet implemented")
        return "not yet implemente"

    def kill(self, **kwargs):
        ValueError("not yet implemented")
        return "not yet implemente"

    def details(self, **kwargs):
        ValueError("not yet implemented")
        return "not yet implemente"

    def clear(self, **kwargs):
        ValueError("not yet implemented")
        return "not yet implemente"

    def refresh(self, **kwargs):
        ValueError("not yet implemented")
        return "not yet implemente"


class LauncherShell(LauncherProvider):

    def run(self, **kwargs):

        script = kwargs["script"]
        output = subprocess.check_output("script", shell=True)

        return output


class Launcher(ListResource):

    def __init__(self, kind):

        if kind.lower() in ["sh", "shell"]:
            return LauncherShell
        else:
            ValueError("not yet implemented")
            return "not yet implemente"


