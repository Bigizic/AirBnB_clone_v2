#!/usr/bin/python3
"""Fabric script that distributes an archive to a web server
"""

from os.path import exists
from fabric.api import *

env.user = "ubuntu"
env.hosts = ['54.82.132.33', '54.197.206.10']


def do_deploy(archive_path):
    """Uploads an archive to the /tmp/ dir of the web server
    uncompress the archive to the dir .... on the web server
    delete the archive from the web server
    delete the symbolic link ...
    create a new symbolic link ...

    Returns:
        False if the file at the path archive_path doesn't exist
        otherwise True if all operations succeds
    """
    if not exists(archive_path):
        return False
    try:
        tar_name = archive_path[9:-4]  # without extension
        tar = archive_path[9:]  # wit extension
        uncompress_dir = f'/data/web_static/releases/{tar_name}/'
        put(archive_path, "/tmp/")
        run(f'mkdir -p {uncompress_dir}/')
        run("tar -xzf /tmp/{} -C {}/".format(archive_path[9:],
            uncompress_dir))
        run("rm /tmp/{}".format(tar))
        run("rm -rf /data/web_static/current")
        run(f'ln -s {uncompress_dir}/ /data/web_static/current')

        return True
    except Exception as e:
        print(e)
        return False