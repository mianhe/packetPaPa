from field import Field
from src.packet.bitsmap import Bitsmap
from src.converter import ip_to_bytes_streams, bytes_stream_to_ip


class IpAddressField(Field):
    def __init__(self,name,value=''):
        Field.__init__(self, name, value)
        
    def pack(self,bitsmap, position):
        bitsmap.append_bytes_stream(ip_to_bytes_streams(self._value))
        return position + 4 * 8
    
    def parse(self,bitsmap,position):
        self._value = bytes_stream_to_ip(bitsmap.get_bytes_as_stream(position, 4))
        return position + 4*8    
    
    @staticmethod
    def is_valid_IP(mac):
        if mac.count('.') != 3:
            return False
        
        for each_byte in mac.split('.'):
            if not(each_byte.isdigit()):
                return False
            if int(each_byte) > 255:
                return False
    
        return True

#######################################################################################    
import unittest

class TestIpAdressField(unittest.TestCase):
    def test_pack_IP_addess(self):
        bits_map = Bitsmap()
        ip_address_field = IpAddressField('ip','1.2.3.255')
        self.assertEqual(ip_address_field.pack(bits_map, 1),33)
        self.assertEqual(bits_map.get_bits(1, 32) ,0x010203ff)
        
    def test_pack_empty_addess(self):
        bits_map = Bitsmap()
        ip_address_field = IpAddressField('ip','0.0.0.0')
        self.assertEqual(ip_address_field.pack(bits_map, 1),33)
        self.assertEqual(bits_map.get_bits(1, 32) ,0x00000000)
    
    def test_parse_IP_address(self):
        field = IpAddressField('ip')
        self.assertEqual(field.parse(Bitsmap('\x80\x02\x03\xff'),1),33)
        self.assertEqual(field._value,'128.2.3.255')   
    
    if __name__ == '__main__':
        unittest.main()