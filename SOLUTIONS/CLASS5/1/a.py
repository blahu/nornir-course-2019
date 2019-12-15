"""
12345678901234567890123456789012345678901234567890123456789012345678901234567890
"""
from nornir import InitNornir
from nornir.core.filter import F
from nornir.core.task import Result
from nornir.plugins.tasks import networking, text
from nornir.plugins.functions.text import print_result

def get_command(task):
    r = task.run(
        task=networking.netmiko_send_command,
        command_string="show ip interface brief")
    import ipdb; ipdb.set_trace()
    if 'syntax error' in r.result:
        print("?")
        raise ValueError("Junos says syntax error")

def main():
    nr = InitNornir(config_file="../../config.yaml")
    nr = nr.filter(name="srx2")
    #print(nr.inventory.hosts.keys())

    results = nr.run(task=get_command)
    #print_result(results)

    print("Success!")

if __name__ == '__main__':
    main()
