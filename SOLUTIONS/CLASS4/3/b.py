from nornir import InitNornir
from nornir.plugins.tasks import networking, text
from nornir.core.filter import F
from nornir.plugins.functions.text import print_result
from pprint import pprint
import argparse

from nornir.core.task import Result


def options_parse():
    parser = argparse.ArgumentParser(description='Add vlan')
    parser.add_argument('id', type=int, help='vlan_id')
    parser.add_argument('name', type=str, help='vlan_name')
    args = parser.parse_args()
    return args.id, args.name

def add_vlan(task, vlan_id, vlan_name):
    vlan_config = [f"vlan {vlan_id}", f"name {vlan_name}"]

    if task.host.platform == 'nxos':
        show_vlan=f"show vlan id {vlan_id}"
    if task.host.platform == 'eos':
        show_vlan=f"show vlan {vlan_id}"
    
    r=task.run(task=networking.netmiko_send_command,
        command_string=show_vlan,
        use_textfsm=True
    )
    
    result = Result(host=task.host)
    result.changed = False

    if isinstance(r.result, str) and 'not found' in r.result:
        ### create new vlan
        task.run(task=networking.netmiko_send_config, 
            config_commands=vlan_config
        )
        result.changed = True


    if isinstance(r.result, list):
        ### vlan exists, check name
        if r.result[0]['name'] != vlan_name:
            ### update vlan name
            task.run(task=networking.netmiko_send_config, 
                config_commands=vlan_config
            )
            result.changed = True

    return result

def main():
    vlan_id, vlan_name = options_parse()
    print(f"vlan_id={vlan_id}")
    print(f"vlan_name={vlan_name}")
    nr=InitNornir(config_file="../../config.yaml")
    nr=nr.filter(F(platform="eos")|F(platform="nxos"))
    print(nr.inventory.hosts.keys())
    results=nr.run(task=add_vlan, vlan_id=vlan_id, vlan_name=vlan_name)
    print_result(results)

if __name__ == '__main__':
    main()
