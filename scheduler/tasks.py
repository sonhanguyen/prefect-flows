from invoke import task
import importlib
import pexpect
import sys


def prefect_start(_):
    child = pexpect.spawn('prefect server start', timeout=600)
    child.logfile = sys.stdout.buffer
    child.expect('Building schema complete!')


def prefect_agent(c):
    c.run('prefect agent start')


@task
def register(c):
    importlib.import_module('flows')


@task
def stop(c):
    dirname="$(dirname {__file__})"

    c.run(f"""
        #cd {dirname}
        cd .venv/lib/python*/site-packages/prefect/cli
        docker-compose down
    """)


@task
def dev(c):
    prefect_start(c)
    register(c)
    c.run('prefect backend server')
    prefect_agent(c)
