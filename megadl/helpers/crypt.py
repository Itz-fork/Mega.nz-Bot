# Copyright (c) 2021 - Present Itz-fork
# Author: https://github.com/Itz-fork
# Project: https://github.com/Itz-fork/Mega.nz-Bot
# Description: Decryption functions
# Credits: https://github.com/Itz-fork/pyro-mega.py/blob/master/src/mega/crypto.py

import re
import json
import base64
import struct
import codecs
from Crypto.Cipher import AES


def makebyte(x):
    return codecs.latin_1_encode(x)[0]


def makestring(x):
    return codecs.latin_1_decode(x)[0]


def aes_cbc_decrypt(data, key):
    aes_cipher = AES.new(key, AES.MODE_CBC, makebyte("\0" * 16))
    return aes_cipher.decrypt(data)


def str_to_a32(b):
    if isinstance(b, str):
        b = makebyte(b)
    if len(b) % 4:
        b += b"\0" * (4 - len(b) % 4)
    return struct.unpack(">%dI" % (len(b) / 4), b)


def base64_to_a32(s):
    return str_to_a32(base64_url_decode(s))


def base64_url_decode(data):
    data += "=="[(2 - len(data) * 3) % 4 :]
    data = re.sub(r"[-_,]", lambda x: {"-": "+", "_": "/", ",": ""}[x.group()], data)
    return base64.b64decode(data)


def a32_to_str(a):
    return struct.pack(">%dI" % len(a), *a)


def decrypt_attr(attr, key):
    attr = aes_cbc_decrypt(attr, a32_to_str(key))
    attr = makestring(attr)
    attr = attr.rstrip("\0")
    return json.loads(attr[4:]) if attr[:6] == 'MEGA{"' else False


def aes_cbc_decrypt_a32(data, key):
    return str_to_a32(aes_cbc_decrypt(a32_to_str(data), a32_to_str(key)))


def decrypt_key(a, key):
    return sum(
        (aes_cbc_decrypt_a32(a[i : i + 4], key) for i in range(0, len(a), 4)), ()
    )


def decrypt_node_key(key_str: str, shared_key: str):
    if ":" not in key_str:
        return None
    encrypted_key = base64_to_a32(key_str.split(":")[1])
    return decrypt_key(encrypted_key, shared_key)
