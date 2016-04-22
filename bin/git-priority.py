#!/usr/bin/env python
from pprint import pprint
import json
import requests
import sys

columns = [
    ("priority", "P", 4),
    ("number", "N", 4),
    ("title", "title", 40),
    ("assignee", "assignee", 10),
    ("milestone", "milestone", 10),
    ("labels", "labels", 20)
]

#
# setup format strings
#
header_format = ""
row_format = ""
header_elements = ['']
row_elements = ['']
headers = {}
for (attribute, header, length) in columns:
    headers[attribute] = header
    header_elements.append("{}{}{}{}{}".format("{", header, ":", length, "}"))
    row_elements.append("{}{}{}{}{}".format("{", attribute, ":", length, "}"))
header_elements.append("")
row_elements.append("")
header_format = ' | '.join(header_elements).strip()
row_format = ' | '.join(row_elements).strip()
# print(row_format)
# rint(header_format)


#
# Print header
#
issue = {}
for (attribute, header, length) in columns:
    issue[attribute] = header
print(row_format.format(**issue))
#
# Print header line
#
issue = {}
for (attribute, header, length) in columns:
    issue[attribute] = "-" * length
print(row_format.format(**issue))

table = []

for page in range(1, 2):
    url = 'https://api.github.com/repos/cloudmesh/client/issues?page={}&per_page=100'.format(page)
    r = requests.get(url)
    issues = r.json()

    for issue in issues:
        row = {}
        assignee = issue["assignee"]
        if issue["assignee"] is not None:
            issue["assignee"] = issue["assignee"]["login"]
        else:
            issue["assignee"] = "None"

        if issue["milestone"] is not None:
            issue["milestone"] = issue["milestone"]["title"]
        else:
            issue["milestone"] = "None"

        if issue["labels"] is not None:
            content = []
            for label in issue["labels"]:
                content.append(label["name"])
            issue["labels"] = ", ".join(content)
        else:
            issue["labels"] = "None"

        priority = 999
        if issue["body"] is not None:
            body = issue["body"].splitlines()
            if len(body) >= 1:
                line = str(body[0])

                if "P:" in line:
                    priority = line.split("P:")[1]

        issue["priority"] = int(priority)

        content = ""
        for (attribute, header, length) in columns:
            data = str(issue[attribute])
            if len(data) > length:
                issue[attribute] = data[:length - 3] + "..."
            row[attribute] = issue[attribute]
        table.append(row)

#
# print the table
#

for row in table:
    print(row_format.format(**row))
