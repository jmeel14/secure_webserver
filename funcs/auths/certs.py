from cryptography import x509
from cryptography.x509.oid import NameOID

import notice

from .. import commons
from . import commons_credents
from . import keys

async def gen_new_cert(auths_path, def_data):
    """Returns cryptography.x509.Certificate
    
    Generates a new certificate"""

    state_msgs = def_data["notif_templates"]
    notice.gen_ntc('info', 'mini', commons.formatted_state(state_msgs, 1, 'creating'))
    
    private_key = await keys.assert_key(auths_path, def_data)
    notice.gen_ntc('success', 'mini', commons.formatted_state(state_msgs, 0, 'ready'))

    cert_defs = def_data["self_cert"]
    cert_sign_req = x509.CertificateSigningRequestBuilder(
        subject_name=x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, cert_defs["country"]),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, cert_defs["state"]),
            x509.NameAttribute(NameOID.LOCALITY_NAME, cert_defs["city"]),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, cert_defs["org_name"]),
            x509.NameAttribute(NameOID.ORGANIZATIONAL_UNIT_NAME, cert_defs["org_unit_name"]),
            x509.NameAttribute(NameOID.COMMON_NAME, cert_defs["cname_address"])
        ])
    )
    cert_sign_req.add_extension(x509.SubjectAlternativeName([
        x509.DNSName(cert_defs["cname_address"])
    ]), critical=False)
    cert_req_priv_signed = cert_sign_req.sign(private_key, commons_credents.hashes.SHA256())
    
    if(not isinstance(cert_req_priv_signed, x509.CertificateSigningRequest)):
        raise(TypeError)
    notice.gen_ntc('success', 'mini', commons.formatted_state(state_msgs, 1, 'ready'))
    return cert_req_priv_signed

async def check_cert_exists(auths_path, def_data):
    cert_data = None
    try:
        cert_buffer = open(commons.join_path(auths_path, "self_cert.pem"), "rb")
        cert_data = cert_buffer.read()
        cert_buffer.close()
    except:
        notice.gen_ntc('warn', 'mini', commons.formatted_state(def_data["notif_templates"], 1, "not_found"))
        err_handle = input("A referred certificate was not found. Would you like to create a new one instead? [Y/n]")
        if(err_handle.lower() == "y" or err_handle == ""):
            cert_data = await gen_new_cert(auths_path, def_data)
        else:
            raise FileNotFoundError
    return cert_data

async def assert_cert(auths_path, def_data):
    inst_cert = await check_cert_exists(auths_path, def_data)
    if(not inst_cert):
        inst_cert = await gen_new_cert(auths_path, def_data)
    return {
        "crt": inst_cert,
        "crt_pub": inst_cert.public_key().public_bytes(
            encoding=commons_credents.serialization.Encoding.PEM,
            format=commons_credents.serialization.PublicFormat.SubjectPublicKeyInfo
        )
    }