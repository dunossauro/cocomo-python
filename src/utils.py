from contextlib import contextmanager
from json import loads
from os import chdir, getcwd, makedirs, path
from shutil import rmtree
from subprocess import PIPE, STDOUT, Popen

from httpx import stream


@contextmanager
def temp_path(ppath):
    if not path.exists(ppath):
        makedirs(ppath)

    initial_path = getcwd()
    chdir(ppath)
    yield ppath
    chdir(initial_path)
    rmtree(ppath, ignore_errors=True)


def json_parse(ppath):
    with open(ppath) as libs:
        return loads(libs.read()).items()


def execute_command(cmd):
    p = Popen(cmd.split(), stdout=PIPE, stderr=STDOUT)
    out, err = p.communicate()
    p.wait()
    return out.decode()


def format_regex_package_name(pkg_name):
    return pkg_name.replace('-', '.').replace('_', '.').replace('==', '.')


def download_file(url):
    local_filename = url.split('/')[-1]
    with stream('GET', url) as r:
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_bytes():
                f.write(chunk)
    return local_filename
