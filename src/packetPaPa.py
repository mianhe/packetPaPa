import sys
sys.path.append(sys.path[0][:-4])

from src.packet.fields.bits import BitsField 
from src.packet.fields.dotSplit import DotSplitField
from src.packet.fields.ipAddress import IpAddressField
from src.packet.fields.mac import MacField
from src.packet.fields.tlv import TlvField 
from src.packet.fields.byteStream import ByteStreamField
from src.packet.packet import Packet

from src import log

packet = None
_is_parse_ongoing = None

def open_log():
    log.open_log()

def start_packet():
    '''
    
    '''
    
    global packet
    packet = Packet()
    
    global _is_parse_ongoing
    _is_parse_ongoing = False
    
def pack_packet():
    global packet
    return packet.pack()

def parse_packet(bit_str=''):
    global packet
    global _is_parse_ongoing

    if _is_parse_ongoing:
        packet.resume_parse()
        return
    packet.parse(_convert_robot_input_to_byte_stream(bit_str))
    _is_parse_ongoing = True

def show_packet():
    return str(packet)

def get_value(name):
    global packet
    return packet.get_value(name)

def set_value(name, value):
    global packet    
    if type(packet.get_value(name)) == type (1):
        value = _convert_robot_input_to_int(value)
    packet.set_value(name, value)

def bits(name, length,value=0):
    length = _convert_robot_input_to_int(length)
    value = _convert_robot_input_to_int(value)
    if value >= 2 ** length: 
        raise Exception ('%s is too big for the field %s with bits length of %s'%(value,name,length))  
    
    global packet
    packet.append_field(BitsField(name,length, value))
    
def u8(name,value=0):
    value = _convert_robot_input_to_int(value)
    
    global packet
    packet.append_field(BitsField(name, 8, value))

def u16(name,value=0):
    value = _convert_robot_input_to_int(value)
    global packet
    packet.append_field(BitsField(name, 16, value))

def u32(name,value=0):
    value = _convert_robot_input_to_int(value)
    global packet
    packet.append_field(BitsField(name, 32, value))
    
def ip(name,value='0.0.0.0'):
    global packet
    if value != '' and not IpAddressField.is_valid_IP(value):
        raise Exception ("'%s' is not a valid Ip address, " %value + \
                            "It should be like '#.#.#.#', "+\
                            "and '#' is a digit number between 0 and 255" )
     
    packet.append_field(IpAddressField(name, value))
    
    
def mac(name,value='0:0:0:0:0:0'):
    global packet
    if value != '' and not MacField.is_valid_mac(value):
        raise Exception ("'%s' is not a valid Mac address, " %value + \
                            "It should be like '#:#:#:#:#:#', "+\
                            "and '#' is a hex number between 00 and ff" )
     
    packet.append_field(MacField(name, value))
    
def tlv(name,type_byte_nr=1,length_byte_nr=1,offset=0,type_=0,value=''):
    type_byte_nr = _convert_robot_input_to_int(type_byte_nr)
    length_byte_nr = _convert_robot_input_to_int(length_byte_nr)
    offset = _convert_robot_input_to_int(offset)
    type_ = _convert_robot_input_to_int(type_)

    global packet
    packet.append_field(TlvField(name,type_byte_nr,length_byte_nr,offset,type_,value))
    
def length_value(name,length_byte_nr=1, value=''):
    length_byte_nr = _convert_robot_input_to_int(length_byte_nr)
    
    global packet
    packet.append_field(TlvField(name,0,length_byte_nr,0,0,value))
    
def dot_split(name,value=''):
    global packet
    packet.append_field(DotSplitField(name,value))
    
def byte_stream(name,length,value=''):
    length = _convert_robot_input_to_int(length)
    value = _convert_robot_input_to_byte_stream(value)

    if len(value) > length:
        raise Exception ("the stream passed should be no longer than the length: %s"  %length)
    value += '\x00'*(length - len(value)) 
    
    global packet
    packet.append_field(ByteStreamField(name,length,value))
    

#############################################################################################

def _convert_robot_input_to_int(value):
    if type(value) == type(1):
        return value 

    value = value.strip()
    try:
        if value[0:2].lower() == '0x':
            return int(value,16)
        if value[0:2].lower() == '0b':
            return int(value,2)
        return int(value)
    except:
        raise Exception("parmeter should be int but is %s" %value)

def _convert_robot_input_to_byte_stream(value):
    value = value.strip()
    if(value[0:2] == '\\x'):
        value = value[2:].strip()
        value = value.replace('  ',' ')
        value = value.replace('  ',' ')
        result = ''
        for a in value.split(' '):
            result += chr(int('0x'+a,16))
        return result
    
    if(value[0:2] == '\\h'):
        value = value[2:].replace(' ','')
        result = ''
        position = 0

        while(position <= len(value)-2):
            result += chr(int('0x'+value[position:position+2],16))
            position += 2
        return result
    
    return value

#############################################################################################
import unittest
class TestPacketSimpleBuilder(unittest.TestCase):
    def setUp(self):
        start_packet()
    
    def test_get_set_value(self):
        bits('bits 1-8',8,1)
        u16('short',0x0111)
        self.assertEqual(get_value('bits 1-8'),1)
        set_value('short',0xabcd)
        self.assertEqual(get_value('short'),0xabcd)

    def test_pure_bits_field_packet(self):
        bits('bits 1-2','2','1')
        bits('bits 3-4',2,2)
        bits('bits 5-8',4,5)
        self.assertEqual(pack_packet(),'\x65')
        
        
    def test_pure_bits_field_packet_2(self):
        bits('bits 1-2',4,1)
        bits('bits 3-4',4,15)
        self.assertEqual(pack_packet(),'\x1f')
        
    def test_build_int_field_packet(self):
        u8('byte',0x01)
        u16('short',0x0203)
        u32('long',0x04050607)
        self.assertEqual(pack_packet(),'\x01\x02\x03\x04\x05\x06\x07')
    
    def test_build_cross_byte_value(self):
        bits('head',4,1)
        u16('short',0x0111)
        bits('tail',4,2)
        self.assertEqual(pack_packet(),'\x10\x11\x12')
    
    def test_build_ip_value(self):
        ip('ip','1.2.3.4')
        self.assertEqual(pack_packet(),'\x01\x02\x03\x04')
        
    def test_build_dot_split_value(self):
        dot_split('URL','www.1234.com')
        self.assertEqual(pack_packet(),\
                         '\x03\x77\x77\x77\x04\x31\x32\x33\x34\x03\x63\x6f\x6D\x00')
        
    def test_build_tlv(self):
        tlv('tlv',1,1,2,0x01,'1234') 
        self.assertEqual(pack_packet(),'\x01\x06\x31\x32\x33\x34')
        
    def test_build_lv(self):
        length_value('tlv',2,'1234') 
        self.assertEqual(pack_packet(),'\x00\x04\x31\x32\x33\x34')

    def test_parse_pure_bits_field_packet(self):    
        bits('bits 1-2',2)
        bits('bits 3-4',2)
        bits('bits 5-8',4)
        parse_packet('\x65')
        self.assertEqual(get_value('bits 1-2'),1)
        self.assertEqual(get_value('bits 3-4'),2)

    def test_conver_to_byte_stream(self):
        self.assertEqual(_convert_robot_input_to_byte_stream('\\x 01 02 03'),'\x01\x02\x03')
        self.assertEqual(_convert_robot_input_to_byte_stream('\\x 01'),'\x01')
        self.assertEqual(_convert_robot_input_to_byte_stream(' \\x 01  02   03'),'\x01\x02\x03')
        self.assertEqual(_convert_robot_input_to_byte_stream('\\h 010203040506a7'),'\x01\x02\x03\x04\x05\x06\xa7')
        self.assertEqual(_convert_robot_input_to_byte_stream('\\h ff0000'),'\xff\x00\x00')
        self.assertEqual(_convert_robot_input_to_byte_stream('abc'),'abc')
        self.assertEqual(_convert_robot_input_to_byte_stream('xyz'),'xyz')


#      0  1  2  3  4  5  6  7  8  9  0  1  2  3  4  5
#    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
#    |                      ID                       |
#    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
#    |QR|   Opcode  |AA|TC|RD|RA|   Z    |   RCODE   |
#    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
#    |                    QDCOUNT                    |
#    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
#    |                    ANCOUNT                    |
#    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
#    |                    NSCOUNT                    |
#    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
#    |                    ARCOUNT                    |
#    +--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+--+
class TestProtocolSpecifcPacketBuilder(unittest.TestCase):  
    def setUp(self):
        start_packet()
              
    def test_dns_head(self):
        start_packet
        u16('ID',0xabcd)
        bits('QR',1)
        bits('Opcode',4)
        bits('AA',1)
        bits('TC',1)
        bits('RD',1)
        bits('RA',1)
        bits('Z',3)
        bits('RCODE',4)
        u16('QDCOUNT')
        u16('ANCOUNT')
        u16('NSCOUNT')
        u16('ARCOUNT')
        self.assertEqual(pack_packet(),'\xab\xcd\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
        
if __name__ == '__main__':
    unittest.main()