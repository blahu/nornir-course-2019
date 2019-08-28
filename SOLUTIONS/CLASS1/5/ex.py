from nornir import InitNornir
def my_task(task):
    h=task.host
    print("Hello, it is {}".format(h.hostname))
    print("my dns1={} and dns2={}".format(h['dns1'], h["dns2"]))


if __name__ == '__main__':
    nr=InitNornir()
    nr.run(task=my_task)

