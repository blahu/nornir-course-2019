from nornir import InitNornir
from nornir.core.filter import F

nr=InitNornir(config_file="config.yaml")
print(f"{nr.config.core.num_workers}")
filt = F(groups__contains="ios")
nr = nr.filter(filt)
print(nr.inventory.hosts)

