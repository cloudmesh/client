from sandman import app

from cloudmesh_base.util import path_expand
filename = "sqlite:///{}".format(path_expand("~/.cloudmesh/cloudmesh.db"))

print("database: {}".format(filename))
app.config['SQLALCHEMY_DATABASE_URI'] = filename

from sandman.model import activate

activate()

app.run()