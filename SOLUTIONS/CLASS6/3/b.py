"""
12345678901234567890123456789012345678901234567890123456789012345678901234567890
"""
from nornir import InitNornir
from nornir.core.filter import F
from nornir.core.task import Result
from nornir.plugins.tasks import networking, text
from nornir.plugins.functions.text import print_result

from pprint import pprint as pp
import logging

logger = logging.getLogger('nornir')

def get_command(task):
    logger.info('SSSSTART')
    if task.host.platform == 'junos':
        command='show system uptime | grep time'
    else:
        command='show clock'
        
    r = task.run(
        task=networking.netmiko_send_command,
        command_string=command
    )
    #import ipdb; ipdb.set_trace()


def main():
    nr = InitNornir(config_file="./config.yaml")
    pp(nr.inventory.hosts.items())

    results = nr.run(task=get_command, num_workers=100)
    print_result(results)

    print("Success!")

if __name__ == '__main__':
    main()
