#!/usr/bin/env python
"""Usage:
    swarm start
    swarm allocate --count=N [--name=NAME]
    swarm stop
    swarm kill [ID]
    swarm ping
    swarm queue [all]
    swarm run ID COMMAND
    swarm ps
    swarm hello
    swarm info
    swarm init
    swarm join
    swarm nodes [ID]
    swarm layout

Arguments:
  N      Number workers

Options:
  -h --help

Description:

  Allocation:

     python swarm.py allocate --count=5
        create an allocation on which we run swarm (e.g. 5 nodes)

     python swarm.py quque
        list the allocations.YOu will see th IDs that you need to interact with the allocation

     python swarm.py kill 142
        kills the allocation with the id 142. You will need the ID that you qget via the queue command

     python swarm.py ping
        returns a hardcoded info of the nodes, should be done dynamically. TODO

"""
from __future__ import print_function
import sys

if not  hasattr(sys, 'real_prefix'):
    print("ERROR: please use a virtualenv")
    sys.exit(1)

from docopt import docopt
from os import system
from cloudmesh_client.common.dotdict import dotdict
from pprint import pprint
from cloudmesh_client.common.util import banner
from cloudmesh_client.shell.console import Console
from cloudmesh_client.common.ConfigDict import ConfigDict
from cloudmesh_client.common.Shell import Shell
from cloudmesh_client.common.hostlist import Parameter


def _ssh(command):
    args = command.split(" ")
    r = Shell.ssh(*args)
    return r


def nodes(user, id):
    r = _ssh("india /opt/slurm/bin/squeue -u {user} -h --format=%N".format(**locals())).split("\n")
    return r


def ids(user):
    print (locals())
    args = "india /opt/slurm/bin/squeue -u {user} -h --format=%i".format(**locals()).split(" ")
    r = Shell.ssh(*args).split("\n")
    return r
    #  return Parameter.expand(r)

def jobs(user, allusers=False):
    print (locals())
    if allusers:
        system("ssh india /opt/slurm/bin/squeue".format(**locals()))
    else:
        system("ssh india /opt/slurm/bin/squeue -u {user} ".format(**locals()))

def init_docker(name):
    data = {'worker': name}
    system("ssh -t india ssh -t {worker} sudo docker swarm init".format(**data))

def join_docker(name, master):
    data = {'worker': name,
            'master': master}

    system("ssh -t india ssh -t {worker} sudo docker join {master}".format(**data))

def info_docker(name):
    data = {'worker': name}
    system("ssh -t india ssh -t {worker} sudo docker info".format(**data))

def start_docker(name):
    data = {'worker': name}
    system("ssh -t india ssh -t {worker} sudo systemctl start docker".format(**data))

def stop_docker(name):
    data = {'worker': name}
    system("ssh -t india ssh -t {worker} sudo systemctl stop docker".format(**data))

def ps_docker(name, user):
    jobs('gvonlasz')
    #data = {'worker': name}
    system("ssh -t india ssh -t {name} \"ps aux | grep docker | grep -v grep\"".format(**locals()))

def get_layout(id, user):
    if id is None:
        myjobs = ids(user)
    else:
        myjobs = [id]
    if len(myjobs) > 1:
        print(jobs, len(myjobs))
        Console.error("More than one swarm cluster running, please specify ID")
    n = nodes(user, myjobs[0])[0]
    all_nodes = Parameter.expand(n)

if __name__ == '__main__':
    arguments = docopt(__doc__)

    data = dotdict(arguments)

    data.user = ConfigDict(filename='cloudmesh.yaml')['cloudmesh']['profile']['user']
    data.NAME = data['--name'] or 'swarm'
    data.N = data['--count']

    if data.username in ['TBD']:
        Console.error("cloudmesh.profile.user not set for delta access. Please edit the cloudmesh.yaml file.")

    pprint (data)



    workers = ['d006']
    manager = ['d005']

    if arguments['start']:


        manager, workers = get_layout(data.ID, data.user)
        print (manager, workers)

        for w in workers + manager:
            banner("HOST: " + w)

            data['worker'] = w
            start_docker(w)

    elif arguments['info']:

        for w in workers + manager:
            banner("HOST: " + w)

            data['worker'] = w
            info_docker(w)

    elif arguments['init']:

        for w in manager:
            banner("HOST: " + w)

            data['worker'] = w
            init_docker(w)

    elif arguments['join']:

        for w in workers:
            banner("HOST: " + w)

            data['worker'] = w
            join_docker(w, 'd001')


    elif arguments['ps']:

        for w in workers + manager:
            banner("HOST: " + w)

            data['worker'] = w
            ps_docker(w)

    elif arguments['stop']:

        for w in workers + manager:
            banner("HOST: " + w)

            data['worker'] = w
            stop_docker(w)
            
    elif arguments['ping']:

        for w in workers + manager:
            banner("HOST: " + w)

            data['worker'] = w
            args = "india ssh {worker} hostname".format(**data).split(" ")
            r = Shell.ssh(*args)
            print (r)

    elif arguments['hello']:

        for w in workers + manager:
            banner("HOST: " + w)

            data['worker'] = w
            args = "-t india ssh -t {worker} sudo docker run hello-world".format(**data).split(" ")
            r = Shell.ssh(*args)

            if "Hello from Docker." in r:
                Console.ok("Docker working.")
            else:
                print (r)


    elif arguments['allocate']:

        system("ssh -t india /opt/slurm/bin/salloc --no-shell -J {NAME} -N {N} -p delta".format(**data))
        system("ssh -t india /opt/slurm/bin/squeue")

    elif arguments['kill']:

        if data.ID is None:
            myjobs = ids(data.user)
        else:
            myjobs = [data.ID]

        for j in myjobs:
            data.ID = j
            system("ssh india /opt/slurm/bin/scancel {ID}".format(**data))

        system("ssh india /opt/slurm/bin/squeue")


    elif arguments['nodes']:

        if data.ID is None:
            myjobs = ids(data.user)
        else:
            myjobs = [data.ID]
        print (type(myjobs))
        print ('jjj', myjobs)
        if len(myjobs) > 1:
            print (jobs, len(myjobs))
            Console.error("More than one swarm cluster running, please specify ID")
        n = nodes(data.user, myjobs[0])[0]
        print (n)
        print (Parameter.expand(n))

    elif arguments['queue']:

        #system("ssh india /opt/slurm/bin/squeue | grep {user} ".format(**data))
        if data.all:
            jobs (data.user)
        else:
            jobs(data.user, allusers=True)

        n = ids(data.user)

        print (n)

    elif arguments['run']:

        system(" ssh india -t /opt/slurm/bin/srun --jobid {ID} \"{COMMAND}\"".format(**data))



'''

        
ssh india

# start daeomons on each ost

sudo service docker start


see if the node works

sudo docker pull centos
sudo docker images centos



# stop daemons

sudo service docker start
'''
