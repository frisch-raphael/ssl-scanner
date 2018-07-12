# -*- coding: utf-8 -*-
'''
The MIT License (MIT)

Copyright (c) 2016 HaHwul(하훌)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

# Code below is modified from a2sv CCS Injection test: https://github.com/hahwul/a2sv

import sys
import socket
import time
import struct
from util import getSupportedTLSVersion, addNecessaryExtensionToHello
#Module
dSSL = {
    "SSLv3" : "\x03\x00",
    "TLSv1" : "\x03\x01",
    "TLSv1.1" : "\x03\x02",
    "TLSv1.2" : "\x03\x03",
}

# The following is a complete list of ciphers for the SSLv3 family up to TLSv1.2
ssl3_cipher = dict()
ssl3_cipher['\x00\x00'] = "TLS_NULL_WITH_NULL_NULL"
ssl3_cipher['\x00\x01'] = "TLS_RSA_WITH_NULL_MD5"
ssl3_cipher['\x00\x02'] = "TLS_RSA_WITH_NULL_SHA"
ssl3_cipher['\x00\x03'] = "TLS_RSA_EXPORT_WITH_RC4_40_MD5"
ssl3_cipher['\x00\x04'] = "TLS_RSA_WITH_RC4_128_MD5"
ssl3_cipher['\x00\x05'] = "TLS_RSA_WITH_RC4_128_SHA"
ssl3_cipher['\x00\x06'] = "TLS_RSA_EXPORT_WITH_RC2_CBC_40_MD5"
ssl3_cipher['\x00\x07'] = "TLS_RSA_WITH_IDEA_CBC_SHA"
ssl3_cipher['\x00\x08'] = "TLS_RSA_EXPORT_WITH_DES40_CBC_SHA"
ssl3_cipher['\x00\x09'] = "TLS_RSA_WITH_DES_CBC_SHA"
ssl3_cipher['\x00\x0a'] = "TLS_RSA_WITH_3DES_EDE_CBC_SHA"
ssl3_cipher['\x00\x0b'] = "TLS_DH_DSS_EXPORT_WITH_DES40_CBC_SHA"
ssl3_cipher['\x00\x0c'] = "TLS_DH_DSS_WITH_DES_CBC_SHA"
ssl3_cipher['\x00\x0d'] = "TLS_DH_DSS_WITH_3DES_EDE_CBC_SHA"
ssl3_cipher['\x00\x0e'] = "TLS_DH_RSA_EXPORT_WITH_DES40_CBC_SHA"
ssl3_cipher['\x00\x0f'] = "TLS_DH_RSA_WITH_DES_CBC_SHA"
ssl3_cipher['\x00\x10'] = "TLS_DH_RSA_WITH_3DES_EDE_CBC_SHA"
ssl3_cipher['\x00\x11'] = "TLS_DHE_DSS_EXPORT_WITH_DES40_CBC_SHA"
ssl3_cipher['\x00\x12'] = "TLS_DHE_DSS_WITH_DES_CBC_SHA"
ssl3_cipher['\x00\x13'] = "TLS_DHE_DSS_WITH_3DES_EDE_CBC_SHA"
ssl3_cipher['\x00\x14'] = "TLS_DHE_RSA_EXPORT_WITH_DES40_CBC_SHA"
ssl3_cipher['\x00\x15'] = "TLS_DHE_RSA_WITH_DES_CBC_SHA"
ssl3_cipher['\x00\x16'] = "TLS_DHE_RSA_WITH_3DES_EDE_CBC_SHA"
ssl3_cipher['\x00\x17'] = "TLS_DH_anon_EXPORT_WITH_RC4_40_MD5"
ssl3_cipher['\x00\x18'] = "TLS_DH_anon_WITH_RC4_128_MD5"
ssl3_cipher['\x00\x19'] = "TLS_DH_anon_EXPORT_WITH_DES40_CBC_SHA"
ssl3_cipher['\x00\x1a'] = "TLS_DH_anon_WITH_DES_CBC_SHA"
ssl3_cipher['\x00\x1b'] = "TLS_DH_anon_WITH_3DES_EDE_CBC_SHA"
ssl3_cipher['\x00\x1c'] = "SSL_FORTEZZA_KEA_WITH_NULL_SHA"
ssl3_cipher['\x00\x1d'] = "SSL_FORTEZZA_KEA_WITH_FORTEZZA_CBC_SHA"
ssl3_cipher['\x00\x1e'] = "SSL_FORTEZZA_KEA_WITH_RC4_128_SHA"
ssl3_cipher['\x00\x1E'] = "TLS_KRB5_WITH_DES_CBC_SHA"
ssl3_cipher['\x00\x1F'] = "TLS_KRB5_WITH_3DES_EDE_CBC_SHA"
ssl3_cipher['\x00\x20'] = "TLS_KRB5_WITH_RC4_128_SHA"
ssl3_cipher['\x00\x21'] = "TLS_KRB5_WITH_IDEA_CBC_SHA"
ssl3_cipher['\x00\x22'] = "TLS_KRB5_WITH_DES_CBC_MD5"
ssl3_cipher['\x00\x23'] = "TLS_KRB5_WITH_3DES_EDE_CBC_MD5"
ssl3_cipher['\x00\x24'] = "TLS_KRB5_WITH_RC4_128_MD5"
ssl3_cipher['\x00\x25'] = "TLS_KRB5_WITH_IDEA_CBC_MD5"
ssl3_cipher['\x00\x26'] = "TLS_KRB5_EXPORT_WITH_DES_CBC_40_SHA"
ssl3_cipher['\x00\x27'] = "TLS_KRB5_EXPORT_WITH_RC2_CBC_40_SHA"
ssl3_cipher['\x00\x28'] = "TLS_KRB5_EXPORT_WITH_RC4_40_SHA"
ssl3_cipher['\x00\x29'] = "TLS_KRB5_EXPORT_WITH_DES_CBC_40_MD5"
ssl3_cipher['\x00\x2A'] = "TLS_KRB5_EXPORT_WITH_RC2_CBC_40_MD5"
ssl3_cipher['\x00\x2B'] = "TLS_KRB5_EXPORT_WITH_RC4_40_MD5"
ssl3_cipher['\x00\x2C'] = "TLS_PSK_WITH_NULL_SHA"
ssl3_cipher['\x00\x2D'] = "TLS_DHE_PSK_WITH_NULL_SHA"
ssl3_cipher['\x00\x2E'] = "TLS_RSA_PSK_WITH_NULL_SHA"
ssl3_cipher['\x00\x2F'] = "TLS_RSA_WITH_AES_128_CBC_SHA"
ssl3_cipher['\x00\x30'] = "TLS_DH_DSS_WITH_AES_128_CBC_SHA"
ssl3_cipher['\x00\x31'] = "TLS_DH_RSA_WITH_AES_128_CBC_SHA"
ssl3_cipher['\x00\x32'] = "TLS_DHE_DSS_WITH_AES_128_CBC_SHA"
ssl3_cipher['\x00\x33'] = "TLS_DHE_RSA_WITH_AES_128_CBC_SHA"
ssl3_cipher['\x00\x34'] = "TLS_DH_anon_WITH_AES_128_CBC_SHA"
ssl3_cipher['\x00\x35'] = "TLS_RSA_WITH_AES_256_CBC_SHA"
ssl3_cipher['\x00\x36'] = "TLS_DH_DSS_WITH_AES_256_CBC_SHA"
ssl3_cipher['\x00\x37'] = "TLS_DH_RSA_WITH_AES_256_CBC_SHA"
ssl3_cipher['\x00\x38'] = "TLS_DHE_DSS_WITH_AES_256_CBC_SHA"
ssl3_cipher['\x00\x39'] = "TLS_DHE_RSA_WITH_AES_256_CBC_SHA"
ssl3_cipher['\x00\x3A'] = "TLS_DH_anon_WITH_AES_256_CBC_SHA"
ssl3_cipher['\x00\x3B'] = "TLS_RSA_WITH_NULL_SHA256"
ssl3_cipher['\x00\x3C'] = "TLS_RSA_WITH_AES_128_CBC_SHA256"
ssl3_cipher['\x00\x3D'] = "TLS_RSA_WITH_AES_256_CBC_SHA256"
ssl3_cipher['\x00\x3E'] = "TLS_DH_DSS_WITH_AES_128_CBC_SHA256"
ssl3_cipher['\x00\x3F'] = "TLS_DH_RSA_WITH_AES_128_CBC_SHA256"
ssl3_cipher['\x00\x40'] = "TLS_DHE_DSS_WITH_AES_128_CBC_SHA256"
ssl3_cipher['\x00\x41'] = "TLS_RSA_WITH_CAMELLIA_128_CBC_SHA"
ssl3_cipher['\x00\x42'] = "TLS_DH_DSS_WITH_CAMELLIA_128_CBC_SHA"
ssl3_cipher['\x00\x43'] = "TLS_DH_RSA_WITH_CAMELLIA_128_CBC_SHA"
ssl3_cipher['\x00\x44'] = "TLS_DHE_DSS_WITH_CAMELLIA_128_CBC_SHA"
ssl3_cipher['\x00\x45'] = "TLS_DHE_RSA_WITH_CAMELLIA_128_CBC_SHA"
ssl3_cipher['\x00\x46'] = "TLS_DH_anon_WITH_CAMELLIA_128_CBC_SHA"
ssl3_cipher['\x00\x60'] = "TLS_RSA_EXPORT1024_WITH_RC4_56_MD5"
ssl3_cipher['\x00\x61'] = "TLS_RSA_EXPORT1024_WITH_RC2_CBC_56_MD5"
ssl3_cipher['\x00\x62'] = "TLS_RSA_EXPORT1024_WITH_DES_CBC_SHA"
ssl3_cipher['\x00\x63'] = "TLS_DHE_DSS_EXPORT1024_WITH_DES_CBC_SHA"
ssl3_cipher['\x00\x64'] = "TLS_RSA_EXPORT1024_WITH_RC4_56_SHA"
ssl3_cipher['\x00\x65'] = "TLS_DHE_DSS_EXPORT1024_WITH_RC4_56_SHA"
ssl3_cipher['\x00\x66'] = "TLS_DHE_DSS_WITH_RC4_128_SHA"
ssl3_cipher['\x00\x67'] = "TLS_DHE_RSA_WITH_AES_128_CBC_SHA256"
ssl3_cipher['\x00\x68'] = "TLS_DH_DSS_WITH_AES_256_CBC_SHA256"
ssl3_cipher['\x00\x69'] = "TLS_DH_RSA_WITH_AES_256_CBC_SHA256"
ssl3_cipher['\x00\x6A'] = "TLS_DHE_DSS_WITH_AES_256_CBC_SHA256"
ssl3_cipher['\x00\x6B'] = "TLS_DHE_RSA_WITH_AES_256_CBC_SHA256"
ssl3_cipher['\x00\x6C'] = "TLS_DH_anon_WITH_AES_128_CBC_SHA256"
ssl3_cipher['\x00\x6D'] = "TLS_DH_anon_WITH_AES_256_CBC_SHA256"
ssl3_cipher['\x00\x80'] = "TLS_GOSTR341094_WITH_28147_CNT_IMIT"
ssl3_cipher['\x00\x81'] = "TLS_GOSTR341001_WITH_28147_CNT_IMIT"
ssl3_cipher['\x00\x82'] = "TLS_GOSTR341094_WITH_NULL_GOSTR3411"
ssl3_cipher['\x00\x83'] = "TLS_GOSTR341001_WITH_NULL_GOSTR3411"
ssl3_cipher['\x00\x84'] = "TLS_RSA_WITH_CAMELLIA_256_CBC_SHA"
ssl3_cipher['\x00\x85'] = "TLS_DH_DSS_WITH_CAMELLIA_256_CBC_SHA"
ssl3_cipher['\x00\x86'] = "TLS_DH_RSA_WITH_CAMELLIA_256_CBC_SHA"
ssl3_cipher['\x00\x87'] = "TLS_DHE_DSS_WITH_CAMELLIA_256_CBC_SHA"
ssl3_cipher['\x00\x88'] = "TLS_DHE_RSA_WITH_CAMELLIA_256_CBC_SHA"
ssl3_cipher['\x00\x89'] = "TLS_DH_anon_WITH_CAMELLIA_256_CBC_SHA"
ssl3_cipher['\x00\x8A'] = "TLS_PSK_WITH_RC4_128_SHA"
ssl3_cipher['\x00\x8B'] = "TLS_PSK_WITH_3DES_EDE_CBC_SHA"
ssl3_cipher['\x00\x8C'] = "TLS_PSK_WITH_AES_128_CBC_SHA"
ssl3_cipher['\x00\x8D'] = "TLS_PSK_WITH_AES_256_CBC_SHA"
ssl3_cipher['\x00\x8E'] = "TLS_DHE_PSK_WITH_RC4_128_SHA"
ssl3_cipher['\x00\x8F'] = "TLS_DHE_PSK_WITH_3DES_EDE_CBC_SHA"
ssl3_cipher['\x00\x90'] = "TLS_DHE_PSK_WITH_AES_128_CBC_SHA"
ssl3_cipher['\x00\x91'] = "TLS_DHE_PSK_WITH_AES_256_CBC_SHA"
ssl3_cipher['\x00\x92'] = "TLS_RSA_PSK_WITH_RC4_128_SHA"
ssl3_cipher['\x00\x93'] = "TLS_RSA_PSK_WITH_3DES_EDE_CBC_SHA"
ssl3_cipher['\x00\x94'] = "TLS_RSA_PSK_WITH_AES_128_CBC_SHA"
ssl3_cipher['\x00\x95'] = "TLS_RSA_PSK_WITH_AES_256_CBC_SHA"
ssl3_cipher['\x00\x96'] = "TLS_RSA_WITH_SEED_CBC_SHA"
ssl3_cipher['\x00\x97'] = "TLS_DH_DSS_WITH_SEED_CBC_SHA"
ssl3_cipher['\x00\x98'] = "TLS_DH_RSA_WITH_SEED_CBC_SHA"
ssl3_cipher['\x00\x99'] = "TLS_DHE_DSS_WITH_SEED_CBC_SHA"
ssl3_cipher['\x00\x9A'] = "TLS_DHE_RSA_WITH_SEED_CBC_SHA"
ssl3_cipher['\x00\x9B'] = "TLS_DH_anon_WITH_SEED_CBC_SHA"
ssl3_cipher['\x00\x9C'] = "TLS_RSA_WITH_AES_128_GCM_SHA256"
ssl3_cipher['\x00\x9D'] = "TLS_RSA_WITH_AES_256_GCM_SHA384"
ssl3_cipher['\x00\x9E'] = "TLS_DHE_RSA_WITH_AES_128_GCM_SHA256"
ssl3_cipher['\x00\x9F'] = "TLS_DHE_RSA_WITH_AES_256_GCM_SHA384"
ssl3_cipher['\x00\xA0'] = "TLS_DH_RSA_WITH_AES_128_GCM_SHA256"
ssl3_cipher['\x00\xA1'] = "TLS_DH_RSA_WITH_AES_256_GCM_SHA384"
ssl3_cipher['\x00\xA2'] = "TLS_DHE_DSS_WITH_AES_128_GCM_SHA256"
ssl3_cipher['\x00\xA3'] = "TLS_DHE_DSS_WITH_AES_256_GCM_SHA384"
ssl3_cipher['\x00\xA4'] = "TLS_DH_DSS_WITH_AES_128_GCM_SHA256"
ssl3_cipher['\x00\xA5'] = "TLS_DH_DSS_WITH_AES_256_GCM_SHA384"
ssl3_cipher['\x00\xA6'] = "TLS_DH_anon_WITH_AES_128_GCM_SHA256"
ssl3_cipher['\x00\xA7'] = "TLS_DH_anon_WITH_AES_256_GCM_SHA384"
ssl3_cipher['\x00\xA8'] = "TLS_PSK_WITH_AES_128_GCM_SHA256"
ssl3_cipher['\x00\xA9'] = "TLS_PSK_WITH_AES_256_GCM_SHA384"
ssl3_cipher['\x00\xAA'] = "TLS_DHE_PSK_WITH_AES_128_GCM_SHA256"
ssl3_cipher['\x00\xAB'] = "TLS_DHE_PSK_WITH_AES_256_GCM_SHA384"
ssl3_cipher['\x00\xAC'] = "TLS_RSA_PSK_WITH_AES_128_GCM_SHA256"
ssl3_cipher['\x00\xAD'] = "TLS_RSA_PSK_WITH_AES_256_GCM_SHA384"
ssl3_cipher['\x00\xAE'] = "TLS_PSK_WITH_AES_128_CBC_SHA256"
ssl3_cipher['\x00\xAF'] = "TLS_PSK_WITH_AES_256_CBC_SHA384"
ssl3_cipher['\x00\xB0'] = "TLS_PSK_WITH_NULL_SHA256"
ssl3_cipher['\x00\xB1'] = "TLS_PSK_WITH_NULL_SHA384"
ssl3_cipher['\x00\xB2'] = "TLS_DHE_PSK_WITH_AES_128_CBC_SHA256"
ssl3_cipher['\x00\xB3'] = "TLS_DHE_PSK_WITH_AES_256_CBC_SHA384"
ssl3_cipher['\x00\xB4'] = "TLS_DHE_PSK_WITH_NULL_SHA256"
ssl3_cipher['\x00\xB5'] = "TLS_DHE_PSK_WITH_NULL_SHA384"
ssl3_cipher['\x00\xB6'] = "TLS_RSA_PSK_WITH_AES_128_CBC_SHA256"
ssl3_cipher['\x00\xB7'] = "TLS_RSA_PSK_WITH_AES_256_CBC_SHA384"
ssl3_cipher['\x00\xB8'] = "TLS_RSA_PSK_WITH_NULL_SHA256"
ssl3_cipher['\x00\xB9'] = "TLS_RSA_PSK_WITH_NULL_SHA384"
ssl3_cipher['\x00\xBA'] = "TLS_RSA_WITH_CAMELLIA_128_CBC_SHA256"
ssl3_cipher['\x00\xBB'] = "TLS_DH_DSS_WITH_CAMELLIA_128_CBC_SHA256"
ssl3_cipher['\x00\xBC'] = "TLS_DH_RSA_WITH_CAMELLIA_128_CBC_SHA256"
ssl3_cipher['\x00\xBD'] = "TLS_DHE_DSS_WITH_CAMELLIA_128_CBC_SHA256"
ssl3_cipher['\x00\xBE'] = "TLS_DHE_RSA_WITH_CAMELLIA_128_CBC_SHA256"
ssl3_cipher['\x00\xBF'] = "TLS_DH_anon_WITH_CAMELLIA_128_CBC_SHA256"
ssl3_cipher['\x00\xC0'] = "TLS_RSA_WITH_CAMELLIA_256_CBC_SHA256"
ssl3_cipher['\x00\xC1'] = "TLS_DH_DSS_WITH_CAMELLIA_256_CBC_SHA256"
ssl3_cipher['\x00\xC2'] = "TLS_DH_RSA_WITH_CAMELLIA_256_CBC_SHA256"
ssl3_cipher['\x00\xC3'] = "TLS_DHE_DSS_WITH_CAMELLIA_256_CBC_SHA256"
ssl3_cipher['\x00\xC4'] = "TLS_DHE_RSA_WITH_CAMELLIA_256_CBC_SHA256"
ssl3_cipher['\x00\xC5'] = "TLS_DH_anon_WITH_CAMELLIA_256_CBC_SHA256"
ssl3_cipher['\x00\x00'] = "TLS_EMPTY_RENEGOTIATION_INFO_SCSV"
ssl3_cipher['\xc0\x01'] = "TLS_ECDH_ECDSA_WITH_NULL_SHA"
ssl3_cipher['\xc0\x02'] = "TLS_ECDH_ECDSA_WITH_RC4_128_SHA"
ssl3_cipher['\xc0\x03'] = "TLS_ECDH_ECDSA_WITH_3DES_EDE_CBC_SHA"
ssl3_cipher['\xc0\x04'] = "TLS_ECDH_ECDSA_WITH_AES_128_CBC_SHA"
ssl3_cipher['\xc0\x05'] = "TLS_ECDH_ECDSA_WITH_AES_256_CBC_SHA"
ssl3_cipher['\xc0\x06'] = "TLS_ECDHE_ECDSA_WITH_NULL_SHA"
ssl3_cipher['\xc0\x07'] = "TLS_ECDHE_ECDSA_WITH_RC4_128_SHA"
ssl3_cipher['\xc0\x08'] = "TLS_ECDHE_ECDSA_WITH_3DES_EDE_CBC_SHA"
ssl3_cipher['\xc0\x09'] = "TLS_ECDHE_ECDSA_WITH_AES_128_CBC_SHA"
ssl3_cipher['\xc0\x0a'] = "TLS_ECDHE_ECDSA_WITH_AES_256_CBC_SHA"
ssl3_cipher['\xc0\x0b'] = "TLS_ECDH_RSA_WITH_NULL_SHA"
ssl3_cipher['\xc0\x0c'] = "TLS_ECDH_RSA_WITH_RC4_128_SHA"
ssl3_cipher['\xc0\x0d'] = "TLS_ECDH_RSA_WITH_3DES_EDE_CBC_SHA"
ssl3_cipher['\xc0\x0e'] = "TLS_ECDH_RSA_WITH_AES_128_CBC_SHA"
ssl3_cipher['\xc0\x0f'] = "TLS_ECDH_RSA_WITH_AES_256_CBC_SHA"
ssl3_cipher['\xc0\x10'] = "TLS_ECDHE_RSA_WITH_NULL_SHA"
ssl3_cipher['\xc0\x11'] = "TLS_ECDHE_RSA_WITH_RC4_128_SHA"
ssl3_cipher['\xc0\x12'] = "TLS_ECDHE_RSA_WITH_3DES_EDE_CBC_SHA"
ssl3_cipher['\xc0\x13'] = "TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA"
ssl3_cipher['\xc0\x14'] = "TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA"
ssl3_cipher['\xc0\x15'] = "TLS_ECDH_anon_WITH_NULL_SHA"
ssl3_cipher['\xc0\x16'] = "TLS_ECDH_anon_WITH_RC4_128_SHA"
ssl3_cipher['\xc0\x17'] = "TLS_ECDH_anon_WITH_3DES_EDE_CBC_SHA"
ssl3_cipher['\xc0\x18'] = "TLS_ECDH_anon_WITH_AES_128_CBC_SHA"
ssl3_cipher['\xc0\x19'] = "TLS_ECDH_anon_WITH_AES_256_CBC_SHA"
ssl3_cipher['\xC0\x1A'] = "TLS_SRP_SHA_WITH_3DES_EDE_CBC_SHA"
ssl3_cipher['\xC0\x1B'] = "TLS_SRP_SHA_RSA_WITH_3DES_EDE_CBC_SHA"
ssl3_cipher['\xC0\x1C'] = "TLS_SRP_SHA_DSS_WITH_3DES_EDE_CBC_SHA"
ssl3_cipher['\xC0\x1D'] = "TLS_SRP_SHA_WITH_AES_128_CBC_SHA"
ssl3_cipher['\xC0\x1E'] = "TLS_SRP_SHA_RSA_WITH_AES_128_CBC_SHA"
ssl3_cipher['\xC0\x1F'] = "TLS_SRP_SHA_DSS_WITH_AES_128_CBC_SHA"
ssl3_cipher['\xC0\x20'] = "TLS_SRP_SHA_WITH_AES_256_CBC_SHA"
ssl3_cipher['\xC0\x21'] = "TLS_SRP_SHA_RSA_WITH_AES_256_CBC_SHA"
ssl3_cipher['\xC0\x22'] = "TLS_SRP_SHA_DSS_WITH_AES_256_CBC_SHA"
ssl3_cipher['\xC0\x23'] = "TLS_ECDHE_ECDSA_WITH_AES_128_CBC_SHA256"
ssl3_cipher['\xC0\x24'] = "TLS_ECDHE_ECDSA_WITH_AES_256_CBC_SHA384"
ssl3_cipher['\xC0\x25'] = "TLS_ECDH_ECDSA_WITH_AES_128_CBC_SHA256"
ssl3_cipher['\xC0\x26'] = "TLS_ECDH_ECDSA_WITH_AES_256_CBC_SHA384"
ssl3_cipher['\xC0\x27'] = "TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA256"
ssl3_cipher['\xC0\x28'] = "TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA384"
ssl3_cipher['\xC0\x29'] = "TLS_ECDH_RSA_WITH_AES_128_CBC_SHA256"
ssl3_cipher['\xC0\x2A'] = "TLS_ECDH_RSA_WITH_AES_256_CBC_SHA384"
ssl3_cipher['\xC0\x2B'] = "TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256"
ssl3_cipher['\xC0\x2C'] = "TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384"
ssl3_cipher['\xC0\x2D'] = "TLS_ECDH_ECDSA_WITH_AES_128_GCM_SHA256"
ssl3_cipher['\xC0\x2E'] = "TLS_ECDH_ECDSA_WITH_AES_256_GCM_SHA384"
ssl3_cipher['\xC0\x2F'] = "TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256"
ssl3_cipher['\xC0\x30'] = "TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384"
ssl3_cipher['\xC0\x31'] = "TLS_ECDH_RSA_WITH_AES_128_GCM_SHA256"
ssl3_cipher['\xC0\x32'] = "TLS_ECDH_RSA_WITH_AES_256_GCM_SHA384"
ssl3_cipher['\xC0\x33'] = "TLS_ECDHE_PSK_WITH_RC4_128_SHA"
ssl3_cipher['\xC0\x34'] = "TLS_ECDHE_PSK_WITH_3DES_EDE_CBC_SHA"
ssl3_cipher['\xC0\x35'] = "TLS_ECDHE_PSK_WITH_AES_128_CBC_SHA"
ssl3_cipher['\xC0\x36'] = "TLS_ECDHE_PSK_WITH_AES_256_CBC_SHA"
ssl3_cipher['\xC0\x37'] = "TLS_ECDHE_PSK_WITH_AES_128_CBC_SHA256"
ssl3_cipher['\xC0\x38'] = "TLS_ECDHE_PSK_WITH_AES_256_CBC_SHA384"
ssl3_cipher['\xC0\x39'] = "TLS_ECDHE_PSK_WITH_NULL_SHA"
ssl3_cipher['\xC0\x3A'] = "TLS_ECDHE_PSK_WITH_NULL_SHA256"
ssl3_cipher['\xC0\x3B'] = "TLS_ECDHE_PSK_WITH_NULL_SHA384"
ssl3_cipher['\xfe\xfe'] = "SSL_RSA_FIPS_WITH_DES_CBC_SHA"
ssl3_cipher['\xfe\xff'] = "SSL_RSA_FIPS_WITH_3DES_EDE_CBC_SHA"
ssl3_cipher['\xff\xe0'] = "SSL_RSA_FIPS_WITH_3DES_EDE_CBC_SHA"
ssl3_cipher['\xff\xe1'] = "SSL_RSA_FIPS_WITH_DES_CBC_SHA"

def getSSLRecords(strBuf):
    lstRecords = []
    if len(strBuf)>=9:
        sslStatus = struct.unpack('>BHHI', strBuf[0:9])
        iType = (sslStatus[3] & (0xFF000000))>>24
        iRecordLen  = sslStatus[3] & (0x00FFFFFF)
        iShakeProtocol = sslStatus[0]
        iSSLLen = sslStatus[2]
        #log(2,"iSSLLen == %d, len(strBuf) == %d, iRecordLen == %d",iSSLLen,len(strBuf),iRecordLen)
        if (iRecordLen + 5 < iSSLLen):
            #log(2,"Multiple Handshakes")
            lstRecords.append((iShakeProtocol,iType))
            iLoopStopper = 0
            iNextOffset = iRecordLen + 9
            while iNextOffset < len(strBuf):
                iLoopStopper += 1
                iCount = 0
                while ((iNextOffset+4) > len(strBuf) and iCount < 5):
                    #log(2,"Need more data to fill buffer")
                    iCount += 1
                    rule.waitForData()
                    if len(rule.buffer) > 0:
                        strBuf += rule.buffer
                if ((iNextOffset+4) > len(strBuf)):
                    #log(2,"End of message")
                    break
                iTypeAndLen = struct.unpack(">I",strBuf[iNextOffset:iNextOffset+4])[0]
                iRecordLen = iTypeAndLen & (0x00FFFFFF)
                iType = (iTypeAndLen & (0xFF000000))>>24
                lstRecords.append((iShakeProtocol,iType))
                iNextOffset += (iRecordLen + 4)
                if iLoopStopper > 8:
                    break
            return lstRecords
        elif (iRecordLen + 9 < len(strBuf)):
            #log(2,"Multiple Records")
            lstRecords.append((iShakeProtocol,iType))
            iNextOffset = iRecordLen + 9
            iLoopStopper = 0
            while iNextOffset+6 < len(strBuf):
                iLoopStopper += 1
                iShakeProtocol = struct.unpack(">B",strBuf[iNextOffset])[0]
                iRecordLen = struct.unpack(">H",strBuf[iNextOffset+3:iNextOffset+5])[0]
                iType = struct.unpack(">B",strBuf[iNextOffset+5])[0]
                #log(2,"iShakeProto == %d, iRecordLen == %d, iType == %d",iShakeProtocol,iRecordLen,iType)
                lstRecords.append((iShakeProtocol,iType))
                iNextOffset += iRecordLen + 5
                if iLoopStopper > 8:
                    break
            return lstRecords
        elif (iRecordLen + 9 == len(strBuf)):
            #log(2,"Single record")
            sslStatus = checkSSLHeader(strBuf)
            lstRecords.append((sslStatus[0],sslStatus[2]))
            return lstRecords
    return None        
    
def checkSSLHeader(strBuf):
    if len(strBuf)>=6:
        sslStatus = struct.unpack('>BHHI', strBuf[0:9])
        iType = (sslStatus[3] & (0xFF000000))>>24
        iRecordLen  = sslStatus[3] & (0x00FFFFFF)
        iShakeProtocol = sslStatus[0]
        iSSLLen = sslStatus[2]        
        return (iShakeProtocol,iSSLLen,iType,iRecordLen)
    return None

def makeHello(strSSLVer):
    r = "\x16" # Message Type 22
    r += dSSL[strSSLVer]
    strCiphers = "" 
    for c in ssl3_cipher.keys():
        strCiphers += c
    dLen = 43 + len(strCiphers)
    r += struct.pack("!H",dLen)
    h = "\x01"
    strPlen = struct.pack("!L",dLen-4)
    h+=strPlen[1:]
    h+= dSSL[strSSLVer]
    rand = struct.pack("!L", int(time.time()))
    rand += "\x36\x24\x34\x16\x27\x09\x22\x07\xd7\xbe\xef\x69\xa1\xb2"
    rand += "\x37\x23\x14\x96\x27\xa9\x12\x04\xe7\xce\xff\xd9\xae\xbb"
    h+=rand
    h+= "\x00" # No Session ID
    h+=struct.pack("!H",len(strCiphers))
    h+=strCiphers
    h+= "\x01\x00"
    return r+h


def test_ccs(strHost, iPort, strVer):
    strHello = makeHello(strVer)
    print("Testing CCS ",strVer)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((strHost,iPort))
        s.settimeout(5)
    except:
        #showDisplay(displayMode,"Failure connecting to %s:%d." % (strHost,iPort))
        return False

    s.send(addNecessaryExtensionToHello(strHello.encode('hex'), strHost).decode('hex'))
    #print("Sending %s Client Hello" % (strVer))
    iCount = 0
    fServerHello = False
    fCert = False
    fKex = False
    fHelloDone = False
    while iCount<5:
        iCount += 1
    try:
        recv = s.recv(20480)
    except:
        return False
    lstRecords = getSSLRecords(recv)
    #print(lstRecords)
    #strLogMessage = "iCount = %d; lstRecords = %s" % (iCount,lstRecords)
    #log(2,strLogMessage)
    #print(fServerHello,fCert)
    if lstRecords != None and len(lstRecords) > 0:
        for (iShakeProtocol,iType) in lstRecords:
            #print(iShakeProtocol,iType)
            if iShakeProtocol == 22:
                if iType == 2:
                    fServerHello = True
                elif iType == 11:
                    fCert = True
                elif iType == 12:
                    fKex = True
                elif iType == 14:
                    fHelloDone = True
            if (fServerHello and fCert):
                break
    else:
        #log(2, "Handshake missing or invalid.  Aborting.")
        return False
    
    if not (fServerHello and fCert):
        pass
        #showDisplay(displayMode," - [LOG] %s Invalid handshake." % (strLogPre))
    elif len(recv)>0:
        pass
    #print("Received %d bytes. (%d)" % (len(recv),ord(recv[0])))
    if ord(recv[0])==22:
        iCount = 0
        strChangeCipherSpec = "\x14"
        strChangeCipherSpec += dSSL[strVer]
        strChangeCipherSpec += "\x00\x01" # Len
        strChangeCipherSpec += "\x01" # Payload CCS
        #print("Sending Change Cipher Spec")
        print("[CCS] Sending CCS")
        s.send(strChangeCipherSpec)
        fVuln = True
        strLastMessage = ""
        while iCount < 3:
            iCount += 1
            s.settimeout(0.5)
            try:
                recv = ''
                recv = s.recv(20480)
                iCount = 0
            except socket.timeout:
                continue
            except socket.error:
                print("[CCS] Connection closed unexpectedly")
                fVuln = False
                break
            if (recv != None and len(recv)>=7):
                print("[CCS] Received something with length %d" % (len(recv)))
                strLastMessage = recv
                if (ord(recv[0])==21):
                    print("[CCS] Received alert %d" % ord(recv[6]))
                    if ord(recv[6]) == 0x0A or ord(recv[6]) == 0x28:
                        print("[CCS] received unexpected message or handshake failure, OK")
                        fVuln = False
                        break
        if fVuln:
            # Try sending another data and see if decryption / bad_mac is return (which mean CCS got through)
            fVuln = False
            try:
                #s.send('\x15' + dSSL[strVer] + '\x00\x02\x01\x00') # Send close notify ?
                print("[CCS] Sending second message")
                s.send(strChangeCipherSpec)
                iCount = 0
                while iCount < 3:
                    iCount += 1
                    s.settimeout(0.5)
                    try:
                        recv = ''
                        recv = s.recv(20480)
                        iCount = 0
                    except socket.timeout:
                        # If always timeout then OK
                        continue
                    except socket.error:
                        print("[CCS] Connection closed unexpectedly")
                        fVuln = False
                        break
                    if (recv != None and len(recv)>=7):
                        print("[CCS] Received something with length %d" % (len(recv)))
                        strLastMessage = recv
                        if (ord(recv[0])==21):
                            print("[CCS] Received alert %d" % ord(recv[6]))
                            if ord(recv[6]) == 0x15:
                                print("[CCS] Received decryption failure, NOT OK")
                                fVuln = True
                                break
                            elif ord(recv[6]) == 0x14:
                                print("[CCS] Received bad_record_mac, NOT OK")
                                fVuln = True
                                break
                            elif ord(recv[6]) == 0x0A or ord(recv[6]) == 0x28:
                                print("[CCS] received unexpected message or handshake failure, OK")
                                fVuln = False
                                break
                            else :
                                print("[CCS] Receieved some other alert, likely NOT OK")
                                fVuln = True
                                break
            except socket.error:
                print("[CCS] Can't send second message")
                fVuln = False
        if fVuln:
            return True
    try:
        s.close()
    except:
        pass
    return False

class CCSTest :
    def __init__(self, result, host, port) :
        self._result = result
        self._host = host
        self._port = port
    
    def start(self) :
        vuln = False
        for version in getSupportedTLSVersion(self._result) :
            if test_ccs(self._host, self._port,["SSLv3","TLSv1","TLSv1.1","TLSv1.2"][version]) :
                vuln = True
        self._result.addResult('ccs_injection',vuln)

        if self._result.getResult('ccs_injection') :
            self._result.addVulnerability('ccs_injection')