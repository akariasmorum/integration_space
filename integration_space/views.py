from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from pathlib import Path

import importlib.util
import uuid
from multiprocessing import Process
import json

# Create your views here.
def hello(request):
	return HttpResponse('<h3>hello</h3>')



SCRIPT_FOLDER  = (Path(__file__).resolve().parent / 'scripts')
def script_list_view(request):
	return JsonResponse(get_scripts_list(), safe = False)

def process_list_view(request):
	return JsonResponse(get_process_list(), safe = False)

def start_script_view(request):
	name = request.POST.get('name')
	priority = request.POST.get('priority')
	params = request.POST.get('params')	 	
	jP = json.loads(params)

	_start_script(name, priority, jP)
	


def get_scripts_list():
	
	files = SCRIPT_FOLDER.glob('**/*')

	file_list = [file.name for file in files]

	return JsonResponse(file_list, safe=False)

process_list = []
def get_process_list(request):
	return process_list



def _start_script(name, priority, params):
	se = ScriptExecutor(name, priority)

	p = Process(target=se.execute, kwargs = params, name= str(uuid.uuid1()))
	process_list.append(
		{
		'process_name': p.name,
		'pid': p.pid,		
		'script_name': name,
		'params': params 
		})
	p.start()
	p.join()

class ScriptExecutor:

	def __init__(self, name, priority):
		self.name = name
		self.path = SCRIPT_FOLDER / name
		self.priority = priority
	

	def execute(self, **kwargs):
		spec = importlib.util.spec_from_file_location("1", self.name)
		foo = importlib.util.module_from_spec(spec)
		spec.loader.exec_module(foo)
		foo.execute(**kwargs)

		'''
		cmd = 'python3.6 scripts/{0}'.format(self.name)
		process = subprocess.run([cmd], stderr=sys.stderr, stdout=sys.stdout)
		'''	

if __name__ == '__main__':
	_start_script('1.py', 5, {'n': 5})








	




