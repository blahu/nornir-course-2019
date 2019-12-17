"""
12345678901234567890123456789012345678901234567890123456789012345678901234567890
"""
from nornir import InitNornir
from nornir.core.filter import F
from nornir.core.task import Result
from nornir.plugins.tasks import networking, text
from nornir.plugins.functions.text import print_result
from nornir.core.exceptions import NornirSubTaskError

from pprint import pprint as pp

def get_command(task):
    try:
        r = task.run(
            task=text.template_file,
            template="loopback.j2",
            path="./",
            **task.host
        )
        #import ipdb; ipdb.set_trace()
    except NornirSubTaskError as e:
        print(f"exception caught for {task.host}")


def main():
    nr = InitNornir(config_file="./config_b.yaml")
    nr = nr.filter(F(groups__contains="nxos"))
    pp(nr.inventory.hosts.items())

    results = nr.run(task=get_command)
    #print_result(results)

    print("Success!")

if __name__ == '__main__':
    main()
