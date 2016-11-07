#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

from nx import *
from nx.objects import *

from services.watch import get_files
from nx.shell import shell




def check_one(fname):
    sh = shell("ffprobe {} -print_format json -show_format".format(fname))
    dump = json.load(sh.stdout())
    try:
        dur = float(dump["format"]["duration"])
    except:
        print os.path.basename(fname)




def check_all():
    for fname in get_files("/mnt/nx02/media.dir"):
        if os.path.splitext(fname)[1] != ".mov":
            continue
        check_one(fname)


if __name__ == "__main__":
    check_all()
