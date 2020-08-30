from invoke import task
import pexpect
import sys


def prefect_use_local(c):
    c.run('prefect backend server')


def prefect_stop(c):
    c.run('prefect server stop')


def prefect_start(c):
    child = pexpect.spawn('prefect server start', timeout=600)
    child.logfile = sys.stdout.buffer
    child.expect('Building schema complete')


def prefect_agent(c):
    c.run('prefect agent start')


@task
def dev(c):
    prefect_start(c)
    prefect_use_local(c)
    prefect_agent(c)
