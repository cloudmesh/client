"""Usage:
   sw create --count=N
   sw allocate --count=N
   sw terminate
   sw kill ID
   sw ping
   sw queue
   sw run ID COMMAND

Arguments:
  N      Number workers

Options:
  -h --help
"""
from docopt import docopt
from os import system
from cloudmesh_client.common.dotdict import dotdict
from pprint import pprint

def start_docker(name):
    data = {'worker': name}
    system("ssh -t india ssh -t {worker} sudo service docker start".format(**data))

def stop_docker(name):
    data = {'worker': name}
    system("ssh -t india ssh -t {worker} sudo service docker stop".format(**data))

    
if __name__ == '__main__':
    arguments = docopt(__doc__)

    data = dotdict(arguments)
    data.N = data['--count']
    pprint (data)

    workers = ['d003','d004']
    manager = ['d001']

    if arguments['create']:

        for w in workers + manager:
            data['worker'] = w
            start_docker(w)

    elif arguments['terminate']:

        for w in workers:
            data['worker'] = w
            stop_docker(w)
            
    elif arguments['ping']:

        for w in workers:
            data['worker'] = w
            system("ssh india ssh {worker} hostname".format(**data))

    elif arguments['allocate']:

        system("ssh -t india /opt/slurm/bin/salloc --no-shell -N {N} -p delta".format(**data))
        system("ssh -t india /opt/slurm/bin/squeue")

    elif arguments['kill']:

        system("ssh india /opt/slurm/bin/scancel {ID}".format(**data))
        system("ssh india /opt/slurm/bin/squeue")

    elif arguments['queue']:

        system("ssh india /opt/slurm/bin/squeue")

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
