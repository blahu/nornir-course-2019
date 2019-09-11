from nornir import InitNornir
from nornir.core.filter import F
from nornir.core.task import Result
from nornir.plugins.tasks import networking, text
from nornir.plugins.functions.text import print_result

import argparse



def options_parse():
    parser = argparse.ArgumentParser(description='Add vlan')
    parser.add_argument('id', type=int, help='vlan_id')
    parser.add_argument('name', type=str, help='vlan_name')
    args = parser.parse_args()
    return args.id, args.name

def add_vlan(task, vlan_id, vlan_name):
    vlan_config = f"vlan {vlan_id}\nname {vlan_name}\n"

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
    result.failed = False
    result.result = f"Vlan {vlan_id} already set up correctly"

    if isinstance(r.result, str) and 'not found' in r.result:
        ### create new vlan
        task.run(task=networking.napalm_configure,
            configuration=vlan_config
        )
        result.changed = True
        result.result = f"Vlan {vlan_id} not found - create it from scratch"

    if isinstance(r.result, str) and 'Invalid' in r.result:
        result.failed = True
        result.result = f"Vlan {vlan_id} is invalid"

    if isinstance(r.result, list):
        ### vlan exists, check name
        current_name = r.result[0]['name']
        if current_name != vlan_name:
            ### update vlan name
            task.run(task=networking.napalm_configure,
                configuration=vlan_config
            )
            result.changed = True
            result.result = f"Vlan {vlan_id} - wrong name ({current_name}) - updating to {vlan_name}"

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
