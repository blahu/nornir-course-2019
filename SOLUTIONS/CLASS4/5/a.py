from nornir import InitNornir
from nornir.core.filter import F
from nornir.core.task import Result
from nornir.plugins.tasks import networking, text
from nornir.plugins.functions.text import print_result

def get_config(task):
    r = task.run(task=networking.napalm_get,
        getters=["config"],
        getters_options={"config": {"retrieve":"running"}})

    result = Result(host=task.host)
    result.changed = False
    result.failed = False
    result.result = r.result
    return result

def main():
    nr=InitNornir(config_file="../../config.yaml")
    nr=nr.filter(name="arista4")
    print(nr.inventory.hosts.keys())
    results=nr.run(task=get_config)
    print_result(results)

if __name__ == '__main__':
    main()
