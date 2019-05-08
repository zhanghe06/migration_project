#!/usr/bin/env python
# encoding: utf-8

"""
@author: zhanghe
@software: PyCharm
@file: encryption.py
@time: 2019-04-27 13:34
"""


import base64
import binascii
import hashlib

password = '123456'
password_db = '4QrcOUm6Wau+VuBX8g+IPg=='

md5 = hashlib.md5()
md5.update(password)

# md5 2进制
password_md5 = md5.digest()
print('password_md5: %s' % password_md5)

# md5 16进制
password_md5_hex = md5.hexdigest()
print('password_md5_hex: %s' % password_md5_hex)

# 2进制转16进制
password_md5_hex = binascii.b2a_hex(password_md5)
print('password_md5_hex: %s' % password_md5_hex)

# 16进制转2进制
password_md5 = binascii.a2b_hex(password_md5_hex)
print('password_md5: %s' % password_md5)

# base64 encode
password_base64_encode = base64.encodestring(password_md5)
print('password_base64_encode: %s' % password_base64_encode)

# base64 decode
password_base64_decode = base64.decodestring(password_base64_encode)
print('password_base64_decode: %s' % password_base64_decode)


if __name__ == '__main__':
    print('-'*20)
    md5 = hashlib.md5()
    md5.update(password)
    print(md5.hexdigest())
    print(binascii.b2a_hex(base64.decodestring(password_db)))
    print(binascii.b2a_hex(base64.decodestring('1B2M2Y8AsgTpgAmY7PhCfg==')))  # d41d8cd98f00b204e9800998ecf8427e 空密码
    print(binascii.b2a_hex(base64.decodestring('BK2gSjPha3APPXp38kwD1Q==')))  # 04ada04a33e16b700f3d7a77f24c03d5 xa03030037
    print(binascii.b2a_hex(base64.decodestring('Z1fJP/K9zkINPBiNTiBlRg==')))  # 6757c93ff2bdce420d3c188d4e206546

    md5 = hashlib.md5()
    md5.update('Chanjet')
    print(md5.hexdigest())

