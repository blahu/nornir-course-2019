from nornir import InitNornir
from nornir.plugins.tasks import networking, text
from nornir.core.filter import F
from nornir.plugins.functions.text import print_result
from pprint import pprint
import argparse



def options_parse():
    parser = argparse.ArgumentParser(description='Add vlan')
    parser.add_argument('id', type=int, help='vlan_id')
    parser.add_argument('name', type=str, help='vlan_name')
    args = parser.parse_args()
    return args.id, args.name

def add_vlan(task, vlan_id, vlan_name):
    vlan_config = [f"vlan {vlan_id}", f"name {vlan_name}"]
    task.run(task=networking.netmiko_send_config,
        config_commands=vlan_config
    )
    if task.host.platform == 'nxos':
        show_vlan=f"show vlan id {vlan_id}"
    if task.host.platform == 'eos':
        show_vlan=f"show vlan {vlan_id}"
    
    task.run(task=networking.napalm_cli,
        commands=[show_vlan]
    )

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
