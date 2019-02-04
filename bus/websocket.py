import websockets
import asyncio
import time 
from django.conf import settings


def ready_x():
	a = process_browser_transmitter()
	loop = asyncio.get_event_loop()
	loop.run_until_complete(a.ready_y())
	loop.run_forever()	

	
class process_browser_transmitter:

	def __init__(self):
		self.pw_socket = None
		self.wb_socket = None


	async def ready_y(self):

		await asyncio.gather(
			websockets.serve(self.process_ws, 'localhost', settings.PROCESS_TO_SERVER_WS_PORT),
			websockets.serve(self.ws_browser, 'localhost', settings.SERVER_TO_BROWSER_WS_PORT),
		)


	async def process_ws(self, websocket, path):
		'''
			Ждет сообщения от сокета "процессы - сервер вебсокетов"
			и пересылает сообщения сокету "сервер вебсокетов - веб браузер"
		'''

		#при подключении сохранить текущий сокет, чтобы другой мог к этому подключиться

		self.pw_socket = websocket

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
				
		while True:
			mess = await websocket.recv()
			print(mess)
			if self.pw_socket!=None:
				await self.pw_socket.send(mess)
			else:
				print('нет соединения с процессами')	
