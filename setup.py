import os
import getpass
import funcs
import notice

QUESTIONS_TXT = [
    "A valid data definition ('defs.json') was not found in the project's auth folder (PROJ_ROOT/data/auth)",
    "Please specify your project's root folder: ",
	"Please insert the host address for your  secure server: ",
	"Please insert the port to use for the initialization of the server: ",
    "Please insert the port to use for the cert authority server: ",
    "Please insert the port to use for the secure webserver: "
	"Please specify the directory for use as public_html:",
    ["country", "Cert country not found. Specify: "],
    ["state", "Cert state not found. Specify: "],
    ["city", "Cert city not found. Specify: "],
    ["cname_address", "Cert address not found. Specify: "],
    ["org_name", "Cert Organization name not found. Specify: "],
    ["org_unit", "Cert Unit name not found. Specify: "]
]

def iter_input_attrs(dict, prompts):
    print(prompts)
    for prop in dict:
        print(prop)
        # dict[prop] = input(prompts)


async def assert_data(self):
    self.config["defs"] = None
    try:
        self.config["defs"] = await funcs.commons.grab_data(self.runtime["path"])
        self.config["defs"] = {
            "password": getpass.getpass("Insert a password to secure the certificate: ")
        }
        funcs.commons.assert_referable(self.config["defs"], "ports", input, "No ports specified in defs. Enter a new port: ")
        iter_input_attrs(self.config["defs"]["self_cert"], [QUESTIONS_TXT[7:12]])
    except:
        notice.gen_ntc("critical", "title", "Critical failure occurred in loading data.")


async def setup(self):
    self.runtime["path"] = input("Enter directory to launch from: ")
    self.config["defs"] = await funcs.commons.grab_data(
        self.runtime["path"], "defs.json"
    )
    if not self.config["pub_path"]:
        os.makedirs("public", exist_ok=True)
        self.config["pub_path"] = funcs.commons.join_path(
            self.runtime["path"], "public"
        )

    if(not self.runtime["key"]):
        self.servs["auth"]["req"] = ("localhost", self.config["defs"]["ports"][0])
        self.servs["auth"]["ca"] = ("localhost", self.config["defs"]["ports"][1])
        self.servs["auth"]["secure"] = await funcs.auth.assert_auth(
            self.config["defs"],
            self.runtime["path"],
            self.servs["auth"]["ca"]
        )
        with open(funcs.commons.join_path(
            self.config["pub_path"], "cert.crt"
        ), "w") as cert_file:
            cert_file.write(self.servs["auth"]["secure"]["crt_pub"].decode())
        self.runtime["sslContext"] = ""