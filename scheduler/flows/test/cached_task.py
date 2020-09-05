"""
This example demonstrates output caching; our first task returns a random number
but requests to be cached for 1.5 minutes.  Our second task prints whatever input
it is given.

We run our flow on a 1 minute interval schedule and observe that the output of
`return_random_number` only changes every other run, due to output caching.
"""
import datetime
import random

from prefect import Flow, task
from prefect.schedules import IntervalSchedule


@task(cache_for=datetime.timedelta(minutes=1, seconds=30))
def return_random_number():
    return random.random()


@task
def print_number(num):
    print("=" * 50)
    print("Value: {}".format(num))
    print("=" * 50)


schedule = IntervalSchedule(
    start_date=datetime.datetime.utcnow(), interval=datetime.timedelta(minutes=1)
)


flow = Flow("cached-task", schedule=schedule)
flow.set_dependencies(
    task=print_number,
    upstream_tasks=[return_random_number])


flow.visualize(
    format='png',
    filename=__file__.replace('.py', ''))
