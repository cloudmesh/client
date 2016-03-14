#!/usr/bin/env python
from pprint import pprint
import json
import requests


for page in range(1,2):
    url = 'https://api.github.com/repos/cloudmesh/client/issues?page={}&per_page=100'.format(page)
    r = requests.get(url)
    issues = r.json()
    for issue in issues:
        #print (issue)
        #print (type(issue))
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

        issue["priority"] = priority

        print ("| {priority} | {number} | {title} | {assignee} | {milestone} | {labels} |".format(**issue))

    #pprint (issues)
