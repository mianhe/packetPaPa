def ip_to_bytes_streams(value):
    result = ''
    for each_byte in value.split('.'):
        result += chr(int(each_byte))
    return result

def bytes_stream_to_ip(ip_bytes):
    result = ''
    for each_byte in ip_bytes:
        result += str(ord(each_byte))+'.'
    return result[:-1]

def dot_split_to_byte_stream(value):
    result = ''
    for a in value.split('.'):
        result += chr(len(a)) + a
    return result + '\x00'

def byte_stream_to_dot_split(value):
    result = ""
    field_length = ord(value[0])
    byte_position = 1
    while  field_length != 0:
        result = result + value[byte_position: byte_position + field_length] 
        byte_position += field_length
        field_length = ord(value[byte_position])
        byte_position += 1
        if (field_length!=0):
            result += '.'
    return result

def bytes_stream_to_mac(mac_bytes_stream):
    result = ''
    for each_byte in mac_bytes_stream:
        byte_as_hex_string = str(hex(ord(each_byte)))[2:]
        byte_as_hex_string = byte_as_hex_string if len(byte_as_hex_string) == 2 \
                                                else '0'+byte_as_hex_string 
        result += byte_as_hex_string + ':'
    return result[:-1]

def mac_to_bytes_stream(mac):
    result = ''
    for each_byte in mac.split(':'):
        result += chr(int(each_byte.strip(),16))
    return result

def _is_printalbe(char):
    return ord(char) >= 20 and ord(char) <= 126

def to_printable(value):
    if type(value) != type('1'):
        return value
    return value.encode('string_escape')

##############################################################
import unittest

class TestIpAdressField(unittest.TestCase):
    def test_build_IP_addess(self):
        
        print to_printable(0)
        print to_printable('\x80\x00\x3112123\x12\x12\x11\x10\x80')