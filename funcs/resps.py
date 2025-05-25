import re
import json

import notice

REFS = {
    "headers": "./data/resps/resps.json",
    "pages": "./data/resps/pages.json"
}

async def gatherer(ref_type):
    resp_file = open(REFS[ref_type], "r")
    resp_data = resp_file.read()
    resp_file.close()
    return json.loads(resp_data)


async def resp_err(resps_dict, err_name):
    return resps_dict["resp_errors"][err_name].encode()

async def resp_head(resps_dict, resp_status, resp_extras):
    resp_set = [
        resps_dict["template"]["head"], " ",
        resps_dict["template"]["resp_code"][resp_status], "\n"

    ]
    resp_set.extend([prop + ": " + resp_extras[prop] + "\n" for prop in resp_extras])
    resp_set.append("\n\n")
    return "".join(resp_set)

async def resp_body(resps_dict):
    header = await resp_head(resps_dict, "308", { "": "" })
    body = "<h1>Hi.</h1><p>You are now communicating with a secure server.<span style='font-size:24px; font-weight:bold;'></p>"
    return (header + body).encode()

async def process_secure(resps_dict, req_data):
    return await resp_body(resps_dict)