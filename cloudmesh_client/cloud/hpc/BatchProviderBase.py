class BatchProviderBase(object):

    prefix = "job"

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
        cls.jobid = 0
        return 0

    @classmethod
    def incr(cls):
        cls.jobid += 1
        return cls.counter()

    @classmethod
    def jobname(cls, counter=None):
        if counter is None:
            counter = cls.counter()
        data = {
            "counter": counter,
            "prefix": cls.prefix
        }
        return "{prefix}-{conunter}".format(**data)
