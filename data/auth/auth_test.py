from cryptography import x509
from cryptography.hazmat.backends import openssl

def test_key(test_func):
    op_file = open("./ca_key.pem", "rb")
    f_data = op_file.read()
    op_file.close()
    print(test_func(f_data))

def test_cert(test_func):
    op_file = open("./ca_cert.pem", "rb")
    f_data = op_file.read()
    op_file.close()
    print(test_func(f_data))