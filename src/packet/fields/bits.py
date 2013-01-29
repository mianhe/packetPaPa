from field import Field
from src.packet.bitsmap import Bitsmap 

class BitsField(Field):
    def __init__(self,name,bit_length,value=0):
        Field.__init__(self, name, value)
        self._bit_length = bit_length
    
    def pack(self,bitsmap, position):
        bitsmap.assgin_bits(position, self._bit_length, self._value)
        return position + self._bit_length
    
    def parse(self,bitsmap,position):
        self._value = bitsmap.get_bits(position, self._bit_length)
        return position + self._bit_length
    
##################################################################################
import unittest    
class TestBitsField(unittest.TestCase):
    def setUp(self):
        self.bits_map = Bitsmap()

    def test_build_bits(self):
        
        bits_field = BitsField('field',8,0x0a)
        self.assertEqual(bits_field.pack(self.bits_map, 1),9)
        self.assertEqual(self.bits_map.get_bits(1, 8) ,0x0a)
    
    def test_parse_bits(self):
        bits_field = BitsField('field',8)
        self.assertEqual(bits_field.parse(Bitsmap('\x0a\x0b'),9),17)
        self.assertEqual(bits_field._value,0x0b)     
        
if __name__ == '__main__':
    unittest.main()       
