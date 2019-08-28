from nornir import InitNornir
def my_task(task):
    print("Hello, it is {}".format(task.host.hostname))


if __name__ == '__main__':
    nr=InitNornir()
    nr.run(task=my_task)

