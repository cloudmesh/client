class Attributes(object):
    @classmethod
    def get(cls, kind):
        layout = {
            'default': {
                'order': ['user',
                          'category',
                          'name',
                          'value',
                          'updated_at'],
                'header': ['User',
                           'Category',
                           'Name',
                           'Value',
                           'Updated']
            },
            'var': {
                'order': ['user',
                          'name',
                          'value',
                          'updated_at'],
                'header': ['User',
                           'Name',
                           'Value',
                           'Updated']
            },
        }
        if kind in layout:
            order = layout[kind]['order']
            header = layout[kind]['header']
        else:
            order = None
            header = None

        return order, header
