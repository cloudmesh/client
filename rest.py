from cloudmesh_client.db.model import DEFAULT, GROUP, KEY, RESERVATION
from sm import app
from sm.model import register

from cloudmesh_client.common.util import path_expand

filename = "sqlite://{}".format(path_expand("~/.cloudmesh/cloudmesh.db"))

print('FFF', filename)

app.config['SQLALCHEMY_DATABASE_URI'] = filename

register((DEFAULT, GROUP, KEY, RESERVATION))

app.run()
