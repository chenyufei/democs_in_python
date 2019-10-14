#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''
为了安装方便，可以直接使用下面的命令：
pip install crypto pycryptodome
pip uninstall crypto pycryptodome
pip install pycryptodome

而如果你是linux环境，则直接安装pycryptodome即可：
pip install pycryptodome
'''
import ctypes
import sys
from Cryptodome.Hash import CMAC
from Cryptodome.Cipher import AES
import binascii


def get_challenge(appeui, appkey, appnonce):
    secret = binascii.a2b_hex(appkey)
    cobj = CMAC.new(secret, ciphermod=AES)
    msg = binascii.a2b_hex(appeui) + \
          binascii.a2b_hex(str('%08x' % appnonce)) + \
          binascii.a2b_hex(str('%08x' % 0))
    cobj.update(msg)
    btr = cobj.digest()
    challenge = ''
    for x in range(0, 16):
        challenge += ('%02X' % btr[16 - x - 1])
    # print(challenge)
    # challenge = cobj.hexdigest()
    #print(challenge)
    return challenge

