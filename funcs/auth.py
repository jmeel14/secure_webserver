import uuid
import datetime
import json
import socket
import ssl

import notice

from . import commons
from .auths import certs, serv


AUTH_REF = commons.join_path("data", "auth")

async def req_auth_sign(def_data, req_cert, ca_serv_tuple):
    state_msgs = def_data["notif_templates"]
    passw_data = def_data["password"].encode()

    ca_conn = await serv.init_serv(ca_serv_tuple)
    #open(def_datafreq_cert.public_key())
    print(dir(req_cert))

    prep_context = ssl.SSLContext(protocol=ssl.PROTOCOL_TLS_SERVER)
    

async def assert_auth(def_data, root_path, ca_serv_tuple):
    pre_cert = await certs.assert_cert(
        commons.join_path(root_path, AUTH_REF),
        def_data
    )
    return pre_cert

async def auth_listener(trigger_serv, ca_serv_tuple, exit_handler):
    trigger_serv.connect(ca_serv_tuple)
    trigger_serv.send(json.dumps({ "command": "sign", "body": {} }))