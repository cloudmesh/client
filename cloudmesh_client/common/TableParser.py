import json

class TableParser(object):

    def __init__(self,
                 header=True,
                 index=None,
                 change=[(":", "_"),("(", "_"),(")", ""),("/", "_")],
                 strip=True,
                 lower=True,
                 strip_seperator=True,
                 seperator="|"):
        self.output = None
        self.with_header = header
        self.change = change
        self.is_lower = lower
        self.is_strip = strip
        self.index = index
        self.strip_seperator = strip_seperator
        self.seperator = seperator

    def clean(self, str):
        if str == '':
            str = 'None'
        if self.is_lower:
            str = str.lower()
        if self.is_strip:
            str = str.strip()
        if self.strip_seperator:
            str = str.replace(self.seperator, "")
            tmp = str[::-1]
            tmp = tmp.replace(self.seperator, "")
            str = tmp[::-1]

        for convert in self.change:
            str = str.replace(convert[0],convert[1])
        return str

    def parse(self, line):
        self.output = line
        self.lines = self.output.splitlines()
        self.headers = \
            [self.clean(h) for h in self.lines[0].split(self.seperator)]
        self.lines = self.lines[1:]


        i = 0
        self.data = {}
        for line in self.lines:
            data = [h.strip() for h in line.split(self.seperator)]
            entry = {}
            for column in range(0, len(self.headers)):
                entry[self.headers[column]] = data[column]
            if self.index is None:
                self.data[str(i)] = entry
            else:
                self.data[entry[self.index]] = entry
            i += 1

    def json(self):
        return self.data

    def __str__(self):
        return json.dumps(self.data, indent=4, separators=(',', ': '))

if __name__ == "__main__":

    parser = TableParser()
    parser.parse("|a|b|c|\n|1|2|3|")
    print parser.json()
    print parser