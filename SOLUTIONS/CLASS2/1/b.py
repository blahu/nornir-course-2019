from nornir import InitNornir
nr=InitNornir(config_file="config.yaml")
print(f"{nr.config.core.num_workers}")
