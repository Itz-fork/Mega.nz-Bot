# Copyright (c) 2023 Itz-fork
# Author: https://github.com/Itz-fork
# Project: https://github.com/Itz-fork/Mega.nz-Bot
# Description: Decryption functions

# Ported from: https://github.com/Itz-fork/pyro-mega.py/blob/master/src/mega/crypto.py

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
    data = re.sub(r'[-_,]', lambda x: {'-': '+', '_': '/', ',': ''}[x.group()], data)
    return base64.b64decode(data)


def a32_to_str(a):
    return struct.pack(">%dI" % len(a), *a)


def decrypt_attr(attr, key):
    attr = aes_cbc_decrypt(attr, a32_to_str(key))
    attr = makestring(attr)
    attr = attr.rstrip("\0")
    return json.loads(attr[4:]) if attr[:6] == 'MEGA{"' else False
