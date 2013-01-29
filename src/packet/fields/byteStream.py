from field import Field
from src.packet.bitsmap import Bitsmap 
from src.converter import to_printable

class ByteStreamField(Field):
    def __init__(self,name,length,value=''):
        Field.__init__(self, name, value)
        self._byte_nr = length
    
    def pack(self,bitsmap, position):
        bitsmap.append_bytes_stream(self._value)
        return position + self._byte_nr * 8
    
    def parse(self,bitsmap,position):
        self._value = bitsmap.get_bytes_as_stream(position, self._byte_nr)
        return position + self._byte_nr*8
    
    def __str__(self):
        return self._name + ':' +  to_printable(self._value) 
    
##################################################################################
import unittest    
class TestBitsField(unittest.TestCase):
    def setUp(self):
        self.bits_map = Bitsmap()

    def test_build_bytes(self):
        bytes_field = ByteStreamField('field',8,'12345678')
        self.assertEqual(bytes_field.pack(self.bits_map, 1),8*8+1)
        self.assertEqual(self.bits_map.get_bytes_as_stream(1, 8),'12345678')
    
    def test_parse_bits(self):
        bytes_field = ByteStreamField('field',8)
        self.assertEqual(bytes_field.parse(Bitsmap('1234\x00\xc0\x00\x00\xff\xff'),1),8*8+1)
        self.assertEqual(bytes_field._value,'1234\x00\xc0\x00\x00')     

if __name__ == '__main__':
    unittest.main()