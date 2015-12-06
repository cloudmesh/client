from cloudmesh_client.cloud.counter import Counter

class BatchProviderBase(object):

    prefix = "job"
    jobid = 0

    @classmethod
    def queue(cls, **kwargs):
        ValueError("Not yet implemented")

    @classmethod
    def delete(cls, **kwargs):
        ValueError("Not yet implemented")

    @classmethod
    def run(cls, **kwargs):
        ValueError("Not yet implemented")

    @classmethod
    def counter(cls):
        cls.jobid = Counter.get()
        return cls.jobid

    @classmethod
    def incr(cls):
        Counter.incr()
        cls.jobid = Counter.get()
        return cls.jobid

    @classmethod
    def jobname(cls, counter=None):
        if counter is None:
            counter = cls.counter()
        data = {
            "counter": counter,
            "prefix": cls.prefix
        }
        return "{prefix}-{conunter}".format(**data)
