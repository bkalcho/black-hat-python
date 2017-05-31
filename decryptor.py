#!/usr/bin/env python
__author__ = 'kalcho'


import zlib
import base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP


private_key = "###PASTE PRIVATE KEY HERE###"

rsakey = RSA.importKey(private_key)
rsakey = PKCS1_OAEP.new(rsakey)

chunk_size = 256
offset = 0
decrypted = ""
encrypted = base64.b64decode(encrypted)

while offset < len(encrypted):
    decrypted += rsakey.decrypt(encrypted[offset:offset+chunk_size])
    offset += chunk_size

# now we decompress to original
plaintext = zlib.decompress(decrypted)

print plaintext