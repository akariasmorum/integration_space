from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from pathlib import Path

import importlib.util
import uuid
from multiprocessing import Process
import json
from .forms import Start_script_form
import subprocess, signal, time, os


# Create your views here.
def main(request):
	return render(request, 'main.html', context = {'title': 'Главная страница'})	


CURRENT_FOLDER = (Path(__file__).resolve().parent)
SCRIPT_FOLDER  = (CURRENT_FOLDER / 'scripts')


def script_list_view(request):
	return JsonResponse(get_scripts_list(), safe = False)


def process_list_view(request):
	return JsonResponse(get_process_list(), safe = False)


def start_script_view(request):
	if request.method == 'POST':
		form = Start_script_form(request.POST)

		if form.is_valid():
			print('hehei {0}'.format(form.cleaned_data))
			name = form.cleaned_data['name']
			priority = form.cleaned_data['priority']
			params = form.cleaned_data['params']
			print('HEHEI!', name, priority, params)

			jP = json.loads(params) or None

			answer = _start_script(name, priority, jP)

			if answer == True:
				return JsonResponse({'result': 'started'})
			else:
				return JsonResponse({'result': 'Error'})
	else:
		form = Start_script_form()

	return render(request, 'start.html', context = {'title': 'Выполнить скрипт', 'form': form})	


################################

def process_controller_view(request):
	command = request.POST.get('command')
	pid = int(request.POST.get('pid'))
	if command == 'RUN':
		continue_process(pid)
	elif command == 'STOP':
		stop_process(pid)
	elif command == 'TERMINATE':
		terminate_process(pid)		


def _stop_process(pid):
	if process_list[pid] == 'RUNNING':
		os.kill(pid, signal.SIGSTOP)
		process_list[pid]['state'] = 'STOPED'


def _continue_process(pid):
	if process_list[pid] == 'STOPED':
		os.kill(pid, signal.SIGCONT)
		process_list[pid]['state'] = 'RUNNING'    	


def _terminate_process(pid):
	if process_list.get(pid):
		os.kill(pid, signal.SIGTERM)
		delete_process_from_process_list(pid)


def __delete_process_from_process_list(pid):
	process_list.pop(pid, None)


#####################################	

def get_scripts_list():
	
	files = SCRIPT_FOLDER.glob('**/*')

	file_list = [file.name for file in files]

	return file_list


process_list = {}
def get_process_list():
	return process_list


def _start_script(name, priority, params):
	try:
		se = ScriptExecutor(name, priority)
		p = Process(target=se.execute, kwargs = params, name= str(uuid.uuid1()))
	
		p.start()

		process_list[p.pid] =	{
			'process_name': p.name ,					
			'script_name': name,
			'params': params,
			'state': 'RUNNING',
			}

		p.join()

		__delete_process_from_process_list(p.pid);
		return True
		
	except Exception as Process_Execution_Exception:
		print(Process_Execution_Exception)
		return False

########################################################
class ScriptExecutor:

	def __init__(self, name, priority):
		self.name = name
		self.path = CURRENT_FOLDER / name
		self.priority = priority
	

	def execute(self, **kwargs):
		spec = importlib.util.spec_from_file_location("1", self.path)
		foo = importlib.util.module_from_spec(spec)
		spec.loader.exec_module(foo)
		foo.execute(**kwargs)		


if __name__ == '__main__':
	_start_script('1.py', 2, {'n': 10})


class Process_list:

	def __init__(self, ):
		self.process_dict = {}


	def insert_process(self, pid, process_name, script_name, params):
		self.process_dict[pid]= {
			'process_name': process_name ,					
			'script_name': script_name,
			'params': params,
			'state': 'RUNNING',
		}


	def change_process_state(self, pid, STATE):
		self.process_dict[pid]['state'] = STATE


	def delete_process(self, pid):
		self.process_dict.pop(pid, None)




