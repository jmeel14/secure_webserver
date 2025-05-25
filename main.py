import os

import asyncio

import socket
from ssl import SSLError

import funcs
import notice
import setup

class AnsweringServer:
	def __init__(self):
		self.config = {
			"name": None,
			"certs": { "auth": None, "signed": None },
			"serv_tuple": None, "pub_path": None,
			"resps": None
		}
		self.runtime = { "loop": None, "threads": None, "key": None, "ip": None, "path": None }
		self.servs = { "pre": None, "auth": { "req": None, "resp": None }, "secure": None }
		self.alive = False

	async def live(self):
		await setup.setup(self)

		self.config["resps"] = await funcs.resps.gatherer("headers")
		self.config["pages"] = await funcs.resps.gatherer("pages")

	async def terminate_serv(self, sv_conn):
		notice.gen_ntc("warn", "title", "Kill command received. Shutting down connection.")
		sv_conn.send(await funcs.page.err_ready("000"))
		sv_conn.close()

		self.alive = False
		self.serv["secure"].close()

ANSWERING_MACHINE = AnsweringServer()
ANSWERING_MACHINE.runtime["loop"] = asyncio.new_event_loop()
ANSWERING_MACHINE.runtime["loop"].run_until_complete(ANSWERING_MACHINE.live())