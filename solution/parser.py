#!/usr/bin/env python
import json
import os
from sys import stdin, stdout

def message_parser(line):
    # Parse JSON string  to dictionary
    file = open("/home/tesuto/routes.txt", "a+")
    file.seek(0, os.SEEK_END)
    pos = file.tell() - 2
    while pos > 0 and file.read(1) != "\n":
        pos -= 2
        file.seek(pos, os.SEEK_SET)
    if pos > 0:
        file.seek(pos, os.SEEK_SET)
        file.truncate()
    temp_message = json.loads(line)
    if temp_message.has_key('counter'):
        if temp_message["counter"] != 1:
                pretty_json = json.dumps(temp_message, indent=4, sort_keys=True)
                pretty_json = ',\n' + pretty_json
                file.write(pretty_json)
        else:
                pretty_json = json.dumps(temp_message, indent=4, sort_keys=True)
                file.write(pretty_json)
    temp = '\n ]\n} '
    file.write(temp)
    file.close()
    return None

counter = 0
file = open("/home/tesuto/routes.txt", "w")
temp = '{ \n "results" : [ \n ]  \n }'
file.write(temp)
file.close()
while True:
    try:
        line = stdin.readline().strip()

        # When the parent dies we are seeing continual newlines, so we only access so many before stopping
        if line == "":
            counter += 1
            if counter > 100:
                break
            continue
        counter = 0

        message = message_parser(line)

    except (KeyboardInterrupt, SystemExit):
        pass
    except IOError:
        # most likely a signal during readline
        pass
