from cryptography.hazmat.primitives.asymmetric import rsa

from .. import commons
from . import commons_credents
import os

import notice

async def gen_new_key(curr_directory, state_msgs, key_pass):
    """Generates an RSAPrivateKey
    
    Arguments:
        curr_directory (str): current working directory
        state_msgs (dict): status messages
        key_pass (str): password to assign to the key
    
    Example:
        gen_new_key(PROGRAM_PATH, {
            "group": ["Key", "Certificate Signing Request", "Certificate"],
            "status": {
                "not_found": "{} was not found.",
                "found": "{} found.",
                "creating": "Now creating {}.",
                "preparing": "Preparing {} for use.",
                "ready": "{} is ready for use."
            }
        }, "password1234")
        
    Returns:
        RSAPrivateKey
    """
    notice.gen_ntc('info', 'mini', commons.formatted_state(state_msgs, 0, 'creating'))
    key_buffer = rsa.generate_private_key(65537, 2048)
    with open(commons.join_path(curr_directory, "self_priv_key.pem"), "wb") as write_file:
        write_file.write(key_buffer.private_bytes(
            encoding=commons_credents.serialization.Encoding.PEM,
            format=commons_credents.serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=commons_credents.serialization.BestAvailableEncryption(password=key_pass.encode())
        ))
    return key_buffer

async def check_key_exists(auths_path, def_data):
    private_key = None
    try:
        print("Looking at: " + auths_path)
        key_test_buff = open(commons.join_path(auths_path, "self_priv_key.pem"), "rb")
        key_test = key_test_buff.read()
        key_test_buff.close()

        if(len(key_test) < 15):
            notice.gen_ntc('warn', 'mini', "Private key is invalid.")
        else:
            passw_data = def_data["password"].encode()
            notice.gen_ntc('info', 'mini', commons.formatted_state(def_data["notif_templates"], 0, 'preparing'))
            private_key = commons_credents.serialization.load_pem_private_key(key_test, passw_data)
            if(not isinstance(private_key, rsa.RSAPrivateKey)):
                notice.gen_ntc('critical', 'mini', "Key access/serialization failed")
    except FileNotFoundError as PrivateKeyFileError:
        notice.gen_ntc('warn', 'mini', commons.formatted_state(def_data["notif_templates"], 0, "not_found"))
        err_handle = input("A referred key was not found. Would you like to create a new one instead? [Y/n]")
        if(err_handle.lower() == "y" or err_handle == ""):
            private_key = await gen_new_key(
                auths_path,
                def_data["notif_templates"],
                def_data["password"]
            )
        else:
            raise PrivateKeyFileError
    except BaseException as PrivateKeyGenericError:
        notice.gen_ntc('critical', 'mini', "Key access/serialization failed")
        print(PrivateKeyGenericError)
    return private_key

async def assert_key(auths_path, def_data):
    """Returns RSAPrivateKey.
    
    Assumes RSA private key exists and attempts to retrieve it. If not, generates a new one.
    """
    private_key = await check_key_exists(auths_path, def_data)
    if(not private_key):
        private_key = await gen_new_key(auths_path, def_data["notif_templates"], def_data["password"])
    return private_key
