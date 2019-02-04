from django.apps import AppConfig
import asyncio
from multiprocessing import Process

from .websocket import ready_x


class BusConfig(AppConfig):
	name = 'bus'
	
	
	def ready(self):
		p = Process(target=ready_x, args=(), name = 'web_socket_listener')
		p.start()

