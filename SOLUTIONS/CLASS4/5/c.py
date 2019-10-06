
from nornir import InitNornir
from nornir.core.filter import F
from nornir.core.task import Result
from nornir.plugins.tasks import networking, text
from nornir.plugins.functions.text import print_result

def get_config(task):
    r = task.run(task=networking.napalm_get,
        getters=["config"],
        getters_options={"config": {"retrieve":"running"}}
    )
    return r

def set_config(task, config, replace=False):
    r = task.run(task=networking.napalm_configure,
        configuration=config,
        replace=replace,
        dry_run=False
    )
    return r

def main():
    nr=InitNornir(config_file="../../config.yaml")
    nr=nr.filter(name="arista4")
    print(nr.inventory.hosts.keys())
    configlet = '''
        interface Loopback123
            description Hello
    '''
    results=nr.run(task=get_config)
    print_result(results)

    print("x"*10)
    print("Current Config")
    print("x"*10)
    current_config="".join(results["arista4"][0].result[0].result["config"]["running"])
    print(type(current_config))
    print(current_config)
    print("x"*10)

    results=nr.run(task=set_config, config=configlet)
    print_result(results)

    results=nr.run(task=get_config)
    print_result(results)

    results=nr.run(task=set_config, config=current_config, replace=True)
    print_result(results)

if __name__ == '__main__':
    main()
