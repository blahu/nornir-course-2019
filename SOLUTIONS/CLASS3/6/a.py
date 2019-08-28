from nornir import InitNornir
from nornir.core.filter import F
from nornir.plugins.tasks.networking import napalm_get
from pprint import pprint
from nornir.plugins.functions.text import print_result

nr=InitNornir(config_file="../../config.yaml")
nr=nr.filter(F(platform="nxos"))
ar=nr.run(task=napalm_get, 
    getters=["config"],
    getters_options={"config": {"retrieve": "all"}})

print_result(ar)

