from field import Field
from src.packet.bitsmap import Bitsmap
from src.converter import dot_split_to_byte_stream, byte_stream_to_dot_split

class DotSplitField(Field):
    def __init__(self,name,value=''):
        Field.__init__(self, name, value)
        
    def pack(self,bitsmap, position):
        byte_stream = dot_split_to_byte_stream(self._value)
        bitsmap.append_bytes_stream(byte_stream)
        return position + len(byte_stream) * 8
    
    def parse(self,bitsmap,position):
        dot_split_str = byte_stream_to_dot_split(bitsmap.get_bytes__till_end_as_stream(position))
        self._value = dot_split_str
        return (len(dot_split_str)+2)*8+position
    

###############################################################################################    
import unittest

class TestConvert(unittest.TestCase):
    def test_convert_URL_to_bin(self):
        bits_map = Bitsmap()
        dot_split_split_field = DotSplitField('URL','www.1234.com') 
        self.assertEqual(dot_split_split_field.pack(bits_map, 1),(len('www.1234.com')+2)*8+1)
        
        self.assertEqual(bits_map.to_byte_stream(),\
                            '\x03\x77\x77\x77\x04\x31\x32\x33\x34\x03\x63\x6f\x6D\x00')

    def test_parse_IP_address(self):
        dot_split_split_field = DotSplitField('URL')
        self.assertEqual(dot_split_split_field.parse\
                (Bitsmap('\x03\x77\x77\x77\x04\x31\x32\x33\x34\x03\x63\x6f\x6D\x00'),1)\
                                                     ,(len('www.1234.com')+2)*8+1)
        self.assertEqual(dot_split_split_field.value(),'www.1234.com')     

if __name__ == '__main__':
    unittest.main()