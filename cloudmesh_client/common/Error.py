class Error(object):

    @classmethod
    def traceback(cls, error=None, debug=True, trace=True):
        if debug and error is not None:
            print (error)
        if trace:
            import traceback
            print(traceback.format_exc())
