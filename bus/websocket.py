import websockets
import asyncio
import time 

def ready_x():

		start_server = websockets.serve(wsio, 'localhost', 10006)
		asyncio.get_event_loop().run_until_complete(start_server)
		asyncio.get_event_loop().run_forever()


async def wsio(websocket, path):
	
	await asyncio.gather(
		listener(websocket, path),		
		timex(websocket, path),
	)


async def listener(websocket, path):

	while True:
		mess = await websocket.recv()
		print(mess)
	

async def timex(websocket, path):

	while True:
		localtime   = time.localtime()
		timeString  = time.strftime("%Y%m%d%H%M%S", localtime)
		await websocket.send(timeString)		
		await asyncio.sleep(2)	
	