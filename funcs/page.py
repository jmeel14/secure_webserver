import json
import time
import gzip
import re

struct_dict = {
    "head": [
        "HTTP/2 ",
        "Content-Type:text/html;charset=utf-8\n",
        "Content-Encoding:utf-8\n",
        "Keep-Alive:timeout=3\n",
        "Cache-Control:max-age=0, no-cache=no-cache\n\n"
    ],
    "pages": {
        "": "page.html"
    },
    "resources": {
        "": "page.html",
        "style.css": "style.css",
        "script.js": "script.js",
        "favicon.ico": "image/favicon_default.ico",
        "/image/favicon_default.ico": "image/favicon_default.ico"
    },
    "errs": {
        "404": ["Page not found", "An error occurred attempting to retrieve the page you have requested. Are you sure it exists?"],
        "500": ["Internal server error", "An error occurred processing your request. Please try again another time."],
        "000": ["Server shutting down", "The server process has been terminated during your connection, and is shutting down."]
    }
}

async def build_date():
    return f"date:{time.strftime('%Y/%m/%d',time.localtime())}"

async def build_err(err_ref):
    err_set = [
        struct_dict["head"][0], err_ref, "\n\n",
        "<!DOCTYPE html><html><head><title>Jmeel's Neurobot</title></head>",
        "<body>",
        "<h1>" + struct_dict["errs"][err_ref][0] + "</h1>",
        "<p>" + struct_dict["errs"][err_ref][1] + "</p>",
        "</body></html>"
    ]
    return err_set

async def err_ready(err_num):
    err_str = await build_err(err_num)
    return gzip.compress("".join(err_str).encode("utf-8"), 5)

async def sanitize_req(req):
    if(req):
        return re.search('GET \/(.*\.*) HTTP', str(req)).groups()[0]
    else:
        print("Odd, empty request was received.")

async def build_head(page_ref):
    str_set = [
        struct_dict["head"][0], "", "\n",
        await build_date(),
        "".join(struct_dict["head"][1:])
    ]
    if(page_ref in struct_dict["pages"] or page_ref in struct_dict["resources"]):
        str_set[1] = "200"
    else:
        str_set[1] = "404"
        print("WEBSERVER: An invalid page request was made...")
    return "".join(str_set).encode("utf-8")
        

async def build_body(page_ref):
    resp_body = []
    if(page_ref in struct_dict["pages"]):
        resp_doc_head_buff = open("./data/doc_head_template.html", "r")
        resp_doc_head = resp_doc_head_buff.read()
        resp_doc_head_buff.close()
        resp_body.append(resp_doc_head)
    
    if(page_ref in struct_dict["resources"]):
        resp_body_file = open("./data/" + struct_dict["resources"][page_ref], "r")
        resp_body.append(resp_body_file.read())
        resp_body_file.close()
    else:
        if(page_ref):
            print("File access error! Attempted to access:" + page_ref)
            resp_body = await build_err("404")
    print(resp_body)
    return gzip.compress("".join(resp_body).encode("utf-8"), 5)
