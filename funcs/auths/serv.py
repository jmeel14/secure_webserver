import socket
from ..commons import json
from . import commons_credents
import notice

async def init_serv(ca_serv_tuple):
    ca_serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ca_serv.connect(ca_serv_tuple)

    return await greet_serv(ca_serv)

async def greet_serv(ca_serv):
    try:
        ca_serv.send(json.dumps({"req_name": "ack"}).encode())
        resp = ca_serv.recv(32)
        if json.loads(str(resp, "utf-8")) == { "message": "ack" }:
            return ca_serv
    except BaseException as ServerCAConnectionError:
        notice.gen_ntc('critical', 'mini', "Critical failure in attempting to connect with the CA server.")
        print(ServerCAConnectionError)

async def terminate_conn(req):
    req.close()