#!/usr/bin/python3
"""A fabric script that deletes out of dat archives from a web
server
"""
import os
from fabric.api import *

env.hosts = ['35.175.135.46', '100.24.235.105']


def do_clean(number=0):
    """Args:
        number: (int) is the number of the archives
    if number is 0 or 1, keeps most recent version of archive
    if numbr is 2 keep most recent and second most recent
    deletes all unnecessary archives minus the number to keep
    Delete all unnecessary archives in the web server
    """
    try:
        archives = os.listdir("versions/")
        new_list = [i for i in archives]
        int_list = [i.replace('web_static_', '').replace('.tgz', '')
                    for i in new_list]
        if int(number) == 1 or int(number) == 0:
            first_max = max(int_list)
            local("mkdir versions/temp")
            path = f'web_static_{first_max}.tgz'
            local(f'cp versions/{path} versions/temp/')
            local("rm versions/*tgz")
            local("cp versions/temp/*tgz versions/")
            local("rm -rf versions/temp")
            with cd("/data/web_static/releases"):
                archives = run("ls -tr").split()
                archives = [a for a in archives if "web_static_" in a]
                [archives.pop() for i in range(int(number))]
                [run("rm -rf ./{}".format(a)) for a in archives]
        if int(number) == 2:
            first_max = max(int_list)
            int_list.remove(first_max)
            sec_max = max(int_list)
            local("mkdir -p versions/temp")
            path = f'versions/web_static_{first_max}.tgz'
            sec_path = f'versions/web_static_{sec_max}.tgz'
            local(f'cp {path} {sec_path} versions/temp/')
            local("rm versions/*tgz")
            local("cp versions/temp/*tgz versions/")
            local("rm -rf versions/temp")
            with cd("/data/web_static/releases"):
                archives = run("ls -tr").split()
                archives = [a for a in archives if "web_static_" in a]
                [archives.pop() for i in range(int(number))]
                [run("rm -rf ./{}".format(a)) for a in archives]
    except Exception:
        return False
