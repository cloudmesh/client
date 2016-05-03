from __future__ import print_function
from cloudmesh_client.db.CloudmeshDatabase import CloudmeshDatabase, CloudmeshMixin
from sqlalchemy import Column, Date, Integer, String


class WORKFLOW(CloudmeshMixin, CloudmeshDatabase.Base):
    """table to store default values

    if the category is "global" it is meant to be a global variable

    todo: check if its global or general
    """
    __tablename__ = "workflow"
    __kind__ = 'workflow'
    __provider__ = 'general'

    status = Column(String)
    location = Column(String)
    description = Column(String)
    dependency = Column(String)
    threads = Column(String) # we store this as string, you need to convert to and from string to use

    def __init__(self, **kwargs):
        super(WORKFLOW, self).set_defaults(**kwargs)
        self.status = kwargs.get('status', 'defined')
        self.description = kwargs.get('description', None)
        self.dependency = kwargs.get('dependency', None)
        self.threads = kwargs.get('threads', '1')


class DEFAULT(CloudmeshMixin, CloudmeshDatabase.Base):
    """table to store default values

    if the category is "global" it is meant to be a global variable

    todo: check if its global or general
    """
    __tablename__ = "default"
    __kind__ = 'default'
    __provider__ = 'general'

    value = Column(String)

    def __init__(self, **kwargs):
        super(DEFAULT, self).set_defaults(**kwargs)
        self.value = kwargs.get('value', None)


class VAR(CloudmeshMixin, CloudmeshDatabase.Base):
    """table to store peristant variable values
    """
    # name defined in mixin

    __tablename__ = "var"

    __kind__ = 'var'
    __provider__ = 'general'

    value = Column(String)

    def __init__(self, **kwargs):
        super(VAR, self).set_defaults(**kwargs)

        self.value = str(kwargs.get('value'))


class LAUNCHER(CloudmeshMixin, CloudmeshDatabase.Base):
    """table to store default values

    if the category is "global" it is meant to be a global variable

    todo: check if its global or general
    """

    __tablename__ = "launcher"

    __kind__ = 'launcher'
    __provider__ = 'general'

    parameters = Column(String)  # This is the parameter represented as yaml object
    source = Column(String)

    def __init__(self, **kwargs):
        super(LAUNCHER, self).set_defaults(**kwargs)
        self.parameters = kwargs.get('parameters')
        self.source = kwargs.get('source')


class KEY(CloudmeshMixin, CloudmeshDatabase.Base):
    __tablename__ = "key"

    __kind__ = 'key'
    __provider__ = 'general'

    fingerprint = Column(String, unique=True)
    value = Column(String)
    source = Column(String)
    comment = Column(String)
    uri = Column(String)
    is_default = Column(String)

    def __init__(self, **kwargs):
        super(KEY, self).set_defaults(**kwargs)

        self.value = kwargs.get("value")
        self.uri = kwargs.get("uri")
        self.comment = kwargs.get("comment")
        self.fingerprint = kwargs.get("fingerprint")
        self.source = kwargs.get("source")
        self.is_default = kwargs.get("is_default")


class GROUP(CloudmeshMixin, CloudmeshDatabase.Base):
    __tablename__ = "group"

    __kind__ = 'group'
    __provider__ = 'general'

    member = Column(String)
    species = Column(String)

    def __init__(self, **kwargs):
        super(GROUP, self).set_defaults(**kwargs)

        self.member = kwargs.get('member')
        self.species = kwargs.get('species') or 'vm'
        self.category = kwargs.get('category', 'general')
        self.type = 'str'


class RESERVATION(CloudmeshMixin, CloudmeshDatabase.Base):
    __tablename__ = "reservation"

    __kind__ = 'reservation'
    __provider__ = 'general'

    hosts = Column(String)  # should be list of strings
    description = Column(String)
    start_time = Column(String)  # date, time
    end_time = Column(String)  # date, time

    def __init__(self, **kwargs):
        super(RESERVATION, self).set_defaults(**kwargs)
        self.hosts = kwargs.get("hosts")
        self.start_time = kwargs.get("start")
        self.end_time = kwargs.get("end")
        self.description = kwargs.get("description")
        self.project = kwargs.get("project")


class SECGROUPRULE(CloudmeshMixin, CloudmeshDatabase.Base):
    __tablename__ = "secgrouprule"

    __kind__ = 'secgrouprule'
    __provider__ = 'general'

    group = Column(String)  # What is this is this name?
    fromPort = Column(String)
    toPort = Column(String)
    protocol = Column(String)
    cidr = Column(String)
    uuid = Column(String)

    # noinspection PyPep8Naming
    def __init__(self, **kwargs):
        super(SECGROUPRULE, self).set_defaults(**kwargs)
        self.uuid = kwargs.get("uuid")
        self.group = kwargs.get("group")  # What is this is this name?
        self.project = kwargs.get("project")
        self.fromPort = kwargs.get("fromPort")
        self.toPort = kwargs.get("toPort")
        self.protocol = kwargs.get("protocol")
        self.cidr = kwargs.get("cidr")


class BATCHJOB(CloudmeshMixin, CloudmeshDatabase.Base):
    __tablename__ = "batchjob"

    __kind__ = 'batchjob'
    __provider__ = 'general'

    dir = Column(String, default="string")
    nodes = Column(String, default="string")
    output_file = Column(String, default="string")
    queue = Column(String, default="string")
    time = Column(String, default="string")
    cluster = Column(String, default="string")
    sbatch_file_path = Column(String, default="string")
    cmd = Column(String, default="string")
    time = Column(String, default="string")
    group = Column(String, default="string")
    job_id = Column(String, default="string")

    def __init__(self, **kwargs):
        super(BATCHJOB, self).set_defaults(name=name, user=user)
        self.dir = kwargs.get('dir')
        self.nodes = kwargs.get('nodes')
        self.output_file = kwargs.pop('output_file')
        self.queue = kwargs.pop('queue')
        self.time = kwargs.pop('time')
        self.cluster = kwargs.pop('cluster')
        self.sbatch_file_path = kwargs.pop('sbatch_file_path')
        self.cmd = kwargs.pop('cmd')
        self.time = kwargs.pop('time')
        self.group = kwargs.pop('group')
        self.job_id = kwargs.pop('job_id')
