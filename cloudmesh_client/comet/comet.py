from __future__ import print_function
from cloudmesh_client.shell.console import Console
import os
import signal
from cloudmesh_base.Shell import Shell


class Comet(object):
    @staticmethod
    def tunnel(start):
        if start:
            os.system("ssh -L 8080:localhost:80 gregor@nucleus")
        else:
            Comet.kill_tunnel()

    @staticmethod
    def kill_tunnel():
        pid = Comet.find_tunnel()
        if pid is None:
            Console.error("No tunnel to comet found")
        else:
            Console.ok("Killing the tunnel to comet")
            os.kill(pid, signal.SIGTERM)

    @staticmethod
    def status():
        pid = Comet.find_tunnel()
        Console.ok ("Comet tunnel: {:}".format(pid))

    @staticmethod
    def find_tunnel():
        r = Shell.execute("ps", ["-ax"]).split("\n")
        pid = None
        info = None
        for line in r:
            if "localhost" in line and "nucleus" in line:
                info = line
                break
        if info:
            pid = int(info.split(" ", 1)[0])
        return pid
