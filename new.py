#!/bin/python

import datetime
import pathlib
import subprocess
import sys
import os
import toml




if len(sys.argv) > 1:
    title = " ".join(sys.argv[1:])
else:
    title = input("Title? ")

file = title.replace(" ", "-").replace("_","-").lower() # good slugs use only alphanum and -
file = f"{file}.md"

path = pathlib.Path("content") / file
if path.exists():
    raise Exception("File exists", path)

date = datetime.date.today()


tags = set();
for f in pathlib.Path("content").glob("**/*.md"):
    try:
        front_matter = f.read_text().split("+++")[1]
        print (front_matter)
        front_matter = toml.loads(front_matter)
        print (front_matter)
        tags.update(front_matter['taxonomies']['tags'])
    except KeyError:
        pass
tags = ", ".join(map(repr, tags))



path.write_text(
    f"""+++
title               = "{title} TODO"
description         = "TODO"
date                = {date:%Y-%m-%d}
# updated            = 2023-07-29
taxonomies.category = ["Programming", "Using Unix"]
taxonomies.tags     = ["TODO", {tags}]
+++

# {title}

TODO
"""
)

subprocess.Popen(f"nvim +/TODO {path} ", shell=True).wait()
