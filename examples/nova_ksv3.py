from keystoneclient.auth.identity import v3
from keystoneclient import session
from novaclient import client
import os
import requests
requests.packages.urllib3.disable_warnings()

# credentials from sys env or configuration
AUTH_URL = os.getenv("OS_AUTH_URL")
USERNAME = os.getenv("OS_USERNAME")
PASSWORD = os.getenv("OS_PASSWORD")
PROJECT_NAME = os.getenv("OS_PROJECT_NAME")
USER_DOMAIN = os.getenv("OS_USER_DOMAIN_ID")
PROJECT_DOMAIN = os.getenv("OS_PROJECT_DOMAIN_ID")
CERT = os.getenv("OS_CACERT")

# auth to identity v3
ksauth = v3.Password(auth_url=AUTH_URL,
                   username=USERNAME,
                   password=PASSWORD,
                   project_name=PROJECT_NAME,
                   user_domain_name=USER_DOMAIN,
                   project_domain_name=PROJECT_DOMAIN)

# nova client v2 based on previous ks auth
sess = session.Session(auth=ksauth, verify=CERT)
nova = client.Client(2, session=sess)

print nova.servers.list()
print nova.flavors.list()
print nova.images.list()

