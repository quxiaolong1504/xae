# -*- coding: utf8 -*-
import os


def get_valid_port(last_port=10000):
    if last_port == 20000:
        return
    pscmd = "netstat -ntl |grep -v Active| grep -v Proto|awk '{print $4}'|awk -F: '{print $NF}'"
    procs = os.popen(pscmd).read()
    procarr = procs.split("\n")
    tt = last_port + 1
    if tt not in procarr:
        return tt
    else:
        get_valid_port(tt)
