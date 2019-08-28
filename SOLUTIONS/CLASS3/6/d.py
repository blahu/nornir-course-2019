from nornir import InitNornir
from nornir.core.filter import F
from nornir.plugins.tasks.networking import napalm_get
from pprint import pprint as pp
from nornir.plugins.functions.text import print_result

nr=InitNornir(config_file="../../config.yaml")
nr=nr.filter(F(platform="nxos"))
ar=nr.run(task=napalm_get, 
    getters=["config", "facts"],
    getters_options={"config": {"retrieve": "all"}})

a_dict={}
for host in nr.inventory.hosts.keys():
    a_dict[host]={}
    r=ar[host][0].result
    print(host)
    running=r["config"]["running"].splitlines()[4:]
    startup=r["config"]["startup"].splitlines()[4:]
    start_running_match=running == startup
    print(start_running_match)
    a_dict[host] = { 
        'model': r['facts']['model'],
        'start_running_match': start_running_match,
        'uptime': r['facts']['uptime'],
        'vendor': r['facts']['vendor']
    }
pp(a_dict)
