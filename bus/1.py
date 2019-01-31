import multiprocessing
from multiprocessing import Process
import subprocess, signal, time, os

def execute(n):
	print("ex: {0}".format(n))
	current = multiprocessing.current_process()
	
	for x in range(0, n):
		print('Process {0} {1} writes {2}'.format(current.name, current.pid, x))
		time.sleep(1)

def check_pid(pid):
	pass


'''
p = Process(target=f, args=(3, ), name= 'abrakadabra')
p.start()
p.join()'''
