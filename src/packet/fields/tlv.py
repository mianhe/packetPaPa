from field import Field
from src.packet.bitsmap import Bitsmap
from src.converter import to_printable

class TlvField(Field):
    def __init__(self,name,type_byte_nr=1,length_byte_nr=1,length_compensation=0,type_=0,value=''):
        Field.__init__(self, name, value)
        self._type_byte_nr = type_byte_nr 
        self._length_byte_nr = length_byte_nr
        self._type = type_
        self._length_compensation = length_compensation
        self._length = len(value) + length_compensation
        
    def pack(self,bitsmap, position):
        bitsmap.assgin_bits(position, self._type_byte_nr*8, self._type)
        position += self._type_byte_nr * 8 
        
        bitsmap.assgin_bits(position, self._length_byte_nr*8, self._length)
        position += self._length_byte_nr * 8 
        
        bitsmap.append_bytes_stream(self._value)
        position += len(self._value) * 8
        return position

    def parse(self,bitsmap,position):
        self._type = bitsmap.get_bits(position, self._type_byte_nr *8)
        position +=  self._type_byte_nr*8
        
        self._length = bitsmap.get_bits(position, self._length_byte_nr *8) - self._length_compensation
        position +=  self._length_byte_nr*8
        
        self._value = bitsmap.get_bytes_as_stream(position, self._length)
        position +=  self._length*8
        return position
    
    def value(self):
        if self._type_byte_nr == 0:
            return self._value
        return self._type, self._value
    
    def __str__(self):
        if self._type_byte_nr == 0:
            return self._name + ":" + to_printable(self._value)
        
        return self._name + ":" + 'type is ' + str(self._type)+' | value is ' + to_printable(self._value) 
    
#############################################################################
import unittest

class TestTlvField(unittest.TestCase):
    def test_build_TLV_without_offset(self):
        bits_map = Bitsmap()
        tlv_field = TlvField('tlv',1,1,0,0x01,'123\x80') 
        self.assertEqual(tlv_field.pack(bits_map, 1),(1+1+4)*8+ 1)
        self.assertEqual(bits_map.to_byte_stream(),'\x01\x04\x31\x32\x33\x80')
        
    def test_build_TLV_with_offset(self):
        bits_map = Bitsmap()
        tlv_field = TlvField('tlv',1,1,2,0x01,'1234') 
        self.assertEqual(tlv_field.pack(bits_map, 1),(1+1+4)*8+ 1)
        self.assertEqual(bits_map.to_byte_stream(),'\x01\x06\x31\x32\x33\x34')
        
    def test_build_TLV_with_0_type_length(self):
        bits_map = Bitsmap()
        tlv_field = TlvField('tlv',0,1,0,0,'1234') 
        self.assertEqual(tlv_field.pack(bits_map, 1),(1+4)*8+ 1)
        self.assertEqual(bits_map.to_byte_stream(),'\x04\x31\x32\x33\x34')

    def test_parse_TLV(self):
        tlv_field = TlvField('tlv',1,1) 
        self.assertEqual(tlv_field.parse(Bitsmap('\x01\x04\x31\x32\x33\x34'),1),\
                         (1+1+4)*8+1)
        self.assertEqual(tlv_field.value()[1],'1234')
        self.assertEqual(tlv_field.value()[0],0x01)    
        
    def test_parse_TLV_with_2_byte_type(self):
        tlv_field = TlvField('tlv',2,1) 
        self.assertEqual(tlv_field.parse(Bitsmap('\x01\x02\x04\x31\x32\x33\x34'),1),\
                         (2+1+4)*8+1)
        self.assertEqual(tlv_field.value()[1],'1234')
        self.assertEqual(tlv_field.value()[0],0x0102)  

    def test_parse_TLV_with_0_byte_type(self):
        tlv_field = TlvField('tlv',0,2,0) 
        self.assertEqual(tlv_field.parse(Bitsmap('\x00\x02\x01\x02'),1),(2+2)*8+1)
        self.assertEqual(tlv_field.value(),'\x01\x02')     
        
    def test_parse_TLV_with_offset(self):
        tlv_field = TlvField('tlv',2,1,3) 
        self.assertEqual(tlv_field.parse(Bitsmap('\x01\x02\x07\x31\x32\x33\x34'),1),\
                         (2+1+4)*8+1)
        self.assertEqual(tlv_field.value()[1],'1234')
        self.assertEqual(tlv_field.value()[0],0x0102)     

if __name__ == '__main__':
    unittest.main()