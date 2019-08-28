from nornir import InitNornir
from pprint import pprint
nr=InitNornir(config_file="../../config.yaml")
pprint(nr.inventory.hosts.items())
