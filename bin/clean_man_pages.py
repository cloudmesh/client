#!/usr/bin/env python
import sys

TAG = 'Commands'

filename = sys.argv[1]
output = [TAG]
tag_found = False
with open(filename) as file:
    for line in file:
        if tag_found:
            output.append(line.rstrip())
        if not tag_found:
            if TAG in line:
                tag_found = True

content = "\n".join(output)
with open(filename, 'w') as file:
    file.write(content)
