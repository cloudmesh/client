from sqlalchemy import Column, Integer, Unicode, UnicodeText, String
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from __future__ import print_function
from random import choice
from string import letters
import sys
import uuid

debug = False

# engine = create_engine('sqlite:////tmp/test.db', echo=debug)
engine = create_engine('sqlite://')
Base = declarative_base(bind=engine)


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    address = Column(String, nullable=True)
    password = Column(String)
    uuid = Column(String)

    def __init__(self, name, address=None, password=None):
        self.name = name
        self.address = address
        if password is None:
            password = ''.join(choice(letters) for n in xrange(10))
        self.password = password
        self.uuid = str(uuid.uuid4())

Base.metadata.create_all()

Session = sessionmaker(bind=engine)
s = Session()

# create instances of my user object
u = User('gregor')
u.address = '101 somewhere'

u2 = User(u'albert')
u2.password = 'hdjkhdljkvhl'

# testing
s.add_all([u, u2])

s.commit()

# When you query the data back it returns instances of your class:

for user in s.query(User):
    print (user.name, user.password, user.uuid, user.id)
