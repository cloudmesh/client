import os
import sys

from keystoneclient.auth.identity import v2
from keystoneclient import session
from novaclient import client

# Docopt is a library for parsing command line arguments
from docopt import docopt

if __name__ == '__main__':
	
	arguments = docopt(__doc__, version = '0.1.0')
	print(arguments)
	
	OS_AUTH_URL = os.environ['OS_AUTH_URL']
	OS_USERNAME = os.environ['OS_USERNAME']
	OS_PASSWORD = os.environ['OS_PASSWORD']
	OS_TENANT_NAME = os.environ['OS_TENANT_NAME']
	OS_CACERT = os.environ['OS_CACERT']
	VERSION = 2
	

	COMMAND = sys.argv[1]
	SERVER_ID = sys.argv[2]

	## KEYSTONE CLIENT AUTHENTICATE
	#keystone = client.Client(auth_url = OS_AUTH_URL, username = OS_USERNAME, password = OS_PASSWORD, tenant_name = OS_TENANT_NAME)

	## GET TENANT LIST
	#tenant_list = keystone.tenants.list()
	#print tenant_list

	## NOVA CLIENT AUTHENTICATE
	auth = v2.Password(auth_url = OS_AUTH_URL,
					   username = OS_USERNAME,
					   password = OS_PASSWORD,
					   tenant_name = OS_TENANT_NAME)

	sess = session.Session(auth = auth, verify = False)
	nova = client.Client(VERSION, session = sess)

	print('Below are the list of servers')
	print(nova.servers.list(detailed=True))

	server = nova.servers.get(SERVER_ID)

	if COMMAND == 'start':
		#server.start()
		print('Server start request  has been accepted!')

	elif COMMAND == 'stop':
		#server.stop()
		print('Server stop request has been accepted!')

	elif COMMAND == 'reboot':
		#server.reboot(reboot_type='SOFT')
		print('Server reboot request has been accepted!')
