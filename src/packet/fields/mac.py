from field import Field
from src.packet.bitsmap import Bitsmap
from src.converter import bytes_stream_to_mac, mac_to_bytes_stream

class MacField(Field):
    def __init__(self,name,value=''):
        Field.__init__(self, name, value)
        
    def pack(self,bitsmap, position):
        mac_bytes = mac_to_bytes_stream(self._value)
        bitsmap.append_bytes_stream(mac_bytes)
        return position + 6 * 8
    
    def parse(self,bitsmap,position):
        mac_address = bytes_stream_to_mac(bitsmap.get_bytes_as_stream(position, 6))
        self._value = mac_address
        return position + 6*8   
    
    @staticmethod
    def is_valid_mac(mac):
        if mac.count(':') != 5:
            return False
        
        try:
            for each_byte in mac.split(':'):
                int('0x'+ each_byte.strip(),16)
        except:
            return False
        
        return True
    
#######################################################################################    
import unittest

class TestIpAdressField(unittest.TestCase):
    def test_is_valid_mac(self):
        self.assertTrue(MacField.is_valid_mac('12:34:56:78:9a:bc'))
        self.assertTrue(MacField.is_valid_mac('12:34:56:78:9a: bc'))

        self.assertFalse(MacField.is_valid_mac('12:34:56:78:9a:fg'))
        self.assertFalse(MacField.is_valid_mac('12:34:56:78:9a'))
    
    def test_build_MAC_addess(self):
        bits_map = Bitsmap()
        mac_field = MacField('mac','4c:0f:6e:5e:b7:a1')
        self.assertEqual(mac_field.pack(bits_map, 1),6*8 + 1)
        bits_map.get_bytes_as_stream(1, 6)
        self.assertEqual(bits_map.get_bytes_as_stream(1, 6),'\x4c\x0f\x6e\x5e\xb7\xa1')
        
    def test_parse_MAC_address(self):
        field = MacField('mac')
        self.assertEqual(field.parse(Bitsmap('\x4c\x0f\x6e\x5e\xb7\xa1'),1),6*8+1)
        self.assertEqual(field._value,'4c:0f:6e:5e:b7:a1')     
if __name__ == '__main__':
    unittest.main()