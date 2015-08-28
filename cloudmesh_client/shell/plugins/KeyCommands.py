class KeyCommands(object):
    def __init__(self, context):
        # super(self.__class__, self).__init__()
        self.context = context
        if self.context.debug:
            print "init KeyCommand"

    def do_key(self, args):
        print 'executing key'
