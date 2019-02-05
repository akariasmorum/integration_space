from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from pathlib import Path

import importlib.util
import uuid
from multiprocessing import Process, Value
import json
from .forms import Start_script_form
import subprocess, signal, time, os
from django.conf import settings
import websockets
import asyncio

# Create your views here.
def main(request):
	return render(request, 'main.html',  context = {'title': 'Главная страница', 'port': settings.PROCESS_TO_SERVER_WS_PORT})	

def main2(request):
	return render(request, 'main2.html', context = {'title': 'Главная страница', 'port': settings.SERVER_TO_BROWSER_WS_PORT})	



CURRENT_FOLDER = (Path(__file__).resolve().parent)
SCRIPT_FOLDER  = (CURRENT_FOLDER / 'scripts')


class Process_list:

	def __init__(self):
		
		self.process_dict = {}

		''''listener = Process(target = self.conn, args=())
		listener.start()'''
		
		
	def conn(self):
		loop = asyncio.new_event_loop()
		loop.run_until_complete(self.connect_socket())
		loop.run_forever()

	async def connect_socket(self):
		adress = 'ws://localhost:{port}'.format(port = settings.PROCESS_TO_SERVER_WS_PORT)
		async with websockets.connect(adress) as websocket:    		
			while True:
				message = await websocket.recv()
				print(message)



	async def send(self, message):
		adress = 'ws://localhost:{port}'.format(port = settings.PROCESS_TO_SERVER_WS_PORT)
		async with websockets.connect(adress) as websocket:
			print('С ПОДКЛЮЧЕНИЕМ"!')
			await websocket.send(message)

	def send_state_a(self, message):
		loop = asyncio.new_event_loop()
		loop.run_until_complete(self.send(message))
		loop.close()

	def process_controller_view(self, message):
		jR = json.loads(message)
		command = message.get('command')
		pid = message.get('pid')

		if command == 'RUN':
			self.continue_process(pid)
		elif command == 'STOP':
			self.stop_process(pid)
		elif command == 'TERMINATE':
			self.terminate_process(pid)		
	

	def send_state(self):
		print('send state dict:')
		try:
			print(str(self.process_dict))
			send_process = Process(target = self.send_state_a, args = (str(self.process_dict),))
			send_process.start()
			send_process.join()

		except Exception as Ex:
			print(Ex)	

		
	def change_function_wrapper(self):
		self.send_state()
		'''if hasattr(self, '_websocket'):
			self.send_state()			
		else:
			print('Нет сокета для отсылки состояния')	'''

	
	def insert_process(self, pid, process_name, script_name, params):
		self.process_dict[pid]= {
			'process_name': process_name ,					
			'script_name': script_name,
			'params': params,
			'state': 'RUNNING',
		}
		self.change_function_wrapper()

		
	def delete_process(self, pid):
		self.process_dict.pop(pid, None)
		self.change_function_wrapper()


	def stop_process(self, pid):
		if self.process_dict[pid] == 'RUNNING':
			os.kill(pid, signal.SIGSTOP)
			process_dict[pid]['state'] = 'STOPED'
			self.change_function_wrapper()
		else:
			print('already stopped')	


	def continue_process(self, pid):
		if self.process_dict[pid] == 'STOPED':
			os.kill(pid, signal.SIGCONT)
			process_dict[pid]['state'] = 'RUNNING'
			self.change_function_wrapper()
		else:
			print('already running')	


	def terminate_process(self, pid):
		if process_dict.get(pid):
			os.kill(pid, signal.SIGTERM)
			self.delete_process(pid)
			self.change_function_wrapper()
		else:
			print('where is no proccess with such pid')	


	def __delete_process_from_process_list(self, pid):
		process_dict.pop(pid, None)


class process_browser_transmitter:

	def __init__(self):
		
		self.pw_socket = None
		self.wb_socket = None


	async def ready(self):

		await asyncio.gather(
			websockets.serve(self.process_ws, 'localhost', settings.PROCESS_TO_SERVER_WS_PORT),
			websockets.serve(self.ws_browser, 'localhost', settings.SERVER_TO_BROWSER_WS_PORT),
		)


	def send(self, message):
		print('ws message:')
		print(message)
		loop = asyncio.new_event_loop()
		loop.run_until_complete(self.wb_socket.send(message))
		loop.close()


	async def process_ws(self, websocket, path):
		'''
			Ждет сообщения от сокета "процессы - сервер вебсокетов"
			и пересылает сообщения сокету "сервер вебсокетов - веб браузер"
		'''

		#при подключении сохранить текущий сокет, чтобы другой мог к этому подключиться

		self.pw_socket = websocket
		print('ПРОЦЕССЫ ПОДКЛЮЧИЛИСЯ')
		print(self.pw_socket)

		while True:
			mess = await websocket.recv()
			print(mess)
			if self.wb_socket!=None:
				await self.wb_socket.send(mess)
			else:
				print('нет соединения с браузер')	
		

	async def ws_browser(self, websocket, path):
		'''
			Ждет сообщения от сокета "сервер вебсокетов - браузер"
			и пересылает сообщения сокету "процессы  - сервер вебсокетов"
		'''

		#при подключении сохранить текущий сокет, чтобы другой мог к этому подключиться
		
		self.wb_socket = websocket
		print('БРАУЗЕР ПОДКЛЮЧИЛСЯ')
		print(self.wb_socket)
		
		while True:
			mess = await websocket.recv()
			print(mess)
			if self.pw_socket!=None:
				await self.pw_socket.send(mess)
			else:
				print('нет соединения с процессами')	

def ready_x():
	
	loop = asyncio.new_event_loop()
	loop.run_until_complete(websocket_server.ready())
	loop.run_forever()


websocket_server = process_browser_transmitter()
websocket_server_process = Process(target = ready_x, args=())
websocket_server_process.start()

processes = Process_list()

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




#####################################	

def get_scripts_list():
	
	files = SCRIPT_FOLDER.glob('**/*')

	file_list = [file.name for file in files]

	return file_list



def get_process_list():
	return processes.process_dict


def _start_script(name, priority, params):
	try:
		se = ScriptExecutor(name, priority)
		p = Process(target=se.execute, kwargs = params, name= str(uuid.uuid1()))
	
		p.start()

		print(p.name + " started")

		processes.insert_process(
			p.pid,
			p.name ,					
			name,
			params,
		)

		p.join()

		print(p.name + " stoped")
		processes.delete_process(p.pid);

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


