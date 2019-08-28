from nornir import InitNornir
nr=InitNornir()
print(f"{nr.config.core.num_workers}")
