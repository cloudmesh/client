from flask import Flask
from flask.ext.sandboy import Sandboy

from flask.ext.sqlalchemy import SQLAlchemy

from cloudmesh_client.db.model import DEFAULT, GROUP, KEY, RESERVATION

app = Flask(__name__)

from cloudmesh_client.util import path_expand
filename = "sqlite:///{}".format(path_expand("~/.cloudmesh/cloudmesh.db"))

print ("FFF", filename)
app.config['SQLALCHEMY_DATABASE_URI'] = filename



db = SQLAlchemy()
db.init_app(app)
with app.app_context():
    db.create_all()
sandboy = Sandboy(app, db, [DEFAULT, GROUP])
app.run(debug=True)