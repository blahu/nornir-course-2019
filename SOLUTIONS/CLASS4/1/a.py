from nornir import InitNornir
from nornir.plugins.tasks import networking, text
from nornir.plugins.functions.text import print_title, print_result


COMMANDS = { 
    'ios' : 'show version | inc uptime',
    'nxos' : 'show version | inc uptime',
    'eos' : 'show version | inc Uptime',
    'junos': 'show system uptime | match System'
}

def check_uptime(task):
    platform=task.host.platform
    command=COMMANDS[platform]
    r=task.run(task=networking.netmiko_send_command, command_string=command)
    print(f"{task.host} {r.result.strip()}")

def main():
    nr = InitNornir(config_file="../../config.yaml")
    results=nr.run(task=check_uptime)
    #print_result(results)
if __name__ == '__main__':
    main()
