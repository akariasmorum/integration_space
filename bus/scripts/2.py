import subprocess, signal, time, os


def stop_process(pid):
    os.kill(pid, signal.SIGSTOP)
def continue_process(pid):
    os.kill(pid, signal.SIGCONT)
def terminate_process(pid):
    os.kill(pid, signal.SIGTERM)

while True:
    command = input()

    if command == 'exit':
        break

    command = command.split(' ')
    pid = int(command[0])
    com = command[1]

    if com == 'stop':
        stop_process(pid)
    elif com == 'continue':
        continue_process(pid)
    elif com == 'terminate':
        terminate_process(pid)
        
    print("pid: {0}, command: {1}".format(pid, com))
