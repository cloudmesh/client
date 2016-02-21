from sm import app, db


from sm.model import register, Model
from cloudmesh_client.db.model import DEFAULT, GROUP, KEY, RESERVATION


from cloudmesh_client.util import path_expand
filename = "sqlite://{}".format(path_expand("~/.cloudmesh/cloudmesh.db"))

print ('FFF', filename)

app.config['SQLALCHEMY_DATABASE_URI'] = filename


register((DEFAULT, GROUP, KEY, RESERVATION))

app.run()