import json

class TableParser(object):

    def __init__(self,
                 header=True,
                 index=None,
                 change=[(":", "_"),("(", "_"),(")", ""),("/", "_")],
                 strip=True,
                 lower=True,
                 strip_seperator=True,
                 seperator="|",
                 comment_chars="+#"):
        """

        :param header: if true the first line is a header. Not implemented
        :param index: if true, identifies one of the heade column as index
                      for dict key naming
        :param change: an array of tuples of characters that need to be
                       changed to allow key creation in the dict
        :param strip: if true the the lines start and end with the separator
        :param lower: converts headers to lower case
        :param strip_seperator: removes the spaces before and after the
                                separator
        :param seperator: the separator character, default is |
        :param comment_chars: lines starting with this chars will be ignored
        :return:
        """
        self.output = None
        self.with_header = header
        self.change = change
        self.is_lower = lower
        self.is_strip = strip
        self.index = index
        self.strip_seperator = strip_seperator
        self.seperator = seperator
        self.comment_chars = comment_chars

    def clean(self, str):
        """
        :param str: cleans the string
        :return:
        """
        if str == '':
            str = 'None'
        if self.is_lower:
            str = str.lower()
        if self.is_strip:
            str = str.strip()
        for convert in self.change:
            str = str.replace(convert[0],convert[1])
        return str


    def _get_headers(self, line):
        self.output = line
        self.lines = self.output.splitlines()
        self.headers = \
            [self.clean(h) for h in self.lines[0].split(self.seperator)]
        if self.is_strip:
            self.headers = self.headers[1:-1]
        self.lines = self.lines[1:]


    def parse_to_list(self, stream):
        """
        :param stream: converts a stream called line to a list
        :type stream: string
        :return: the list
        """

        self._get_headers(stream)

        i = 0
        self.data = []
        for line in self.lines:
            if line[0] not in  self.comment_chars:
                element = [h.strip() for h in line.split(self.seperator)]
                if self.is_strip:
                    element  = element[1:-1]

                entry = {}
                for column in range(0, len(self.headers)):
                    entry[self.headers[column]] = element[column]
                if self.index is None:
                    entry["_id"] = str(i)
                else:
                    entry["_id"] = self.index
                self.data.append(entry)
                i += 1
        return self.data

    def parse_to_dict(self, stream):
        """

        :param stream: converts a stream called line to a dict
        :type stream: string
        :return: the dict
        """

        self._get_headers(stream)
        i = 0
        self.data = {}
        for line in self.lines:
            if line[0] not in  self.comment_chars:
                element = [h.strip() for h in line.split(self.seperator)]
                if self.is_strip:
                    element  = element[1:-1]
                entry = {}
                for column in range(0, len(self.headers)):
                    entry[self.headers[column]] = element[column]
                if self.index is None:
                    self.data[str(i)] = dict(entry)
                else:
                    self.data[entry[self.index]] = dict(entry)
                i += 1
        return self.data

    def json(self):
        return self.data

    def __str__(self):
        return json.dumps(self.data, indent=4, separators=(',', ': '))

if __name__ == "__main__":

    parser = TableParser()
    d = parser.parse_to_list("|a|b|c|\n|1|2|3|\n+|4|5|6|\n|7|8|9|")
    print d
    print parser.json()
    print parser.headers
    print parser


    parser.parse_to_dict("|a|b|c|\n|1|2|3|\n|4|5|6|")
    print parser.json()

    print parser.headers
    print parser