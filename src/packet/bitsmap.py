import struct

class Bitsmap():
    def __init__(self,bit_str=''):
        self._map = []
        for each_byte in bit_str:
            self._map.append(struct.unpack('B',each_byte)[0])
        
    def _assgin_bit(self,postion,value):
        # value is 1 or 0
        byte_position = (postion-1) / 8
        bit_position = (postion-1) % 8
        
        while len(self._map) < byte_position + 1:
            self._map.append(0)

        if value == 1:
            self._map[byte_position] |= 0b10000000 >> bit_position
        
        if value == 0:
            self._map[byte_position] &= ~(0b10000000 >> bit_position)
    
    def _get_bit(self,postion):
        byte_position = (postion-1) / 8
        bit_position = (postion-1) % 8
        return (self._map[byte_position] >> (8-bit_position-1)) & 0x01 
            
    def assgin_bits(self,postion,bits_nr,value):
        bit_position=0
        while bit_position < bits_nr:
            bit_value = (value >> (bits_nr-1-bit_position)) & 0x01
            self._assgin_bit(postion+bit_position,bit_value)
            bit_position += 1

    def append_bytes_stream(self,byte_stream):
        for each_byte_char in byte_stream:
            self._map.append(ord(each_byte_char))
            
    def append_byte_list(self,byte_list):
        for each_byte in byte_list:
            self._map.append(each_byte)
            
    def get_bits(self,start_position, length):
        bit_nr = 0
        result = 0
        while bit_nr < length:
            result = result << 1
            result |= self._get_bit(start_position+bit_nr)
            bit_nr += 1
        return result
            
    def to_byte_stream(self):
        rtn_buffer = ''
        for each_byte in self._map:
            rtn_buffer += chr(each_byte)
        return rtn_buffer

    def get_bytes_as_stream(self, start_postion, length):
        result = ''
        byte_postion = (start_postion - 1)/8
        for each_byte in self._map[byte_postion:byte_postion+length]:
            result += chr(each_byte) 
        return result
    
    def get_bytes__till_end_as_stream(self, start_postion):
        result = ''
        byte_postion = (start_postion - 1)/8
        for each_byte in self._map[byte_postion:]:
            result += chr(each_byte) 
        return result
    
    def get_bytes_as_list(self, start_postion, length):
        result = []
        byte_postion = (start_postion - 1)/8
        for each_byte in self._map[byte_postion:byte_postion+length]:
            result.append(each_byte) 
        return result
    
##########################################################################   
import unittest

class TestBitsMap(unittest.TestCase):
    def test_init_with_bit_str(self):
        bitmap = Bitsmap('\x01\x02')
        self.assertEqual(bitmap._map[0],0x01)
        self.assertEqual(bitmap._map[1],0x02)
    
    def test_get_bit(self):
        bitmap = Bitsmap('\x01')
        self.assertEqual(bitmap._get_bit(4),0x00)
        self.assertEqual(bitmap._get_bit(8),0x01)
        
    def test_get_bit_in_two_byte(self):
        bitmap = Bitsmap('\x01\x03')
        self.assertEqual(bitmap._get_bit(4),0x00)
        self.assertEqual(bitmap._get_bit(8),0x01)
        self.assertEqual(bitmap._get_bit(16),0x01)
        
    def test_get_bits(self):
        bitmap = Bitsmap('\xf7')
        self.assertEqual(bitmap.get_bits(3,4),0x0D)
        
    def test_get_bits_in_two_byte(self):
        bitmap = Bitsmap('\xff\x7f')
        self.assertEqual(bitmap.get_bits(8,3),0x05)
        
    def test_get_bytes_as_stream(self):
        bitmap = Bitsmap('\x01\x02\x03\x04\x05')
        self.assertEqual(bitmap.get_bytes_as_stream(1*8+1,3),'\x02\x03\x04')
        
    def test_get_bytes_as_list(self):
        bitmap = Bitsmap('\x01\x80\x03\x04\x05')
        self.assertEqual(bitmap.get_bytes_as_list(1*8+1,3),[0x80,0x03,0x04])
        
    def test_assign_one_bit_to_empty(self):
        bitmap = Bitsmap()
        bitmap._assgin_bit(1,1)
        self.assertEqual(bitmap.to_byte_stream(),'\x80')
        
    def test_assign_one_bit_to_second_byte_for_empty_buffer(self):
        bitmap = Bitsmap()
        bitmap._assgin_bit(9,1)
        self.assertEqual(bitmap.to_byte_stream(),'\x00\x80')
        
    def test_assign_one_bit_to_second_byte_for_existing_buffer(self):
        bitmap = Bitsmap()
        bitmap._assgin_bit(9,1)
        bitmap._assgin_bit(9,0)
        self.assertEqual(bitmap.to_byte_stream(),'\x00\x00')
        
    def test_assign_bits_to_empty_signle_byte(self):
        bitmap = Bitsmap()
        bitmap.assgin_bits(1,4,0b10)
        self.assertEqual(bitmap.to_byte_stream(),'\x20')
        
    def test_assign_bits_to_empty_multi_byte(self):
        bitmap = Bitsmap()
        bitmap.assgin_bits(1,11,0x0511)
        self.assertEqual(bitmap.to_byte_stream(),'\xa2\x20')
        
    def test_assign_byte_for_empty_map(self):
        bitmap = Bitsmap()
        bitmap.append_bytes_stream('\x01\x02\x03')
        self.assertEqual(bitmap.to_byte_stream(),'\x01\x02\x03')
    
    def test_assign_byte_after_bits(self):
        bitmap = Bitsmap()
        bitmap.assgin_bits(1,11,0x0511)
        bitmap.append_bytes_stream('\x01\x02\x03')
        self.assertEqual(bitmap.to_byte_stream(),'\xa2\x20\x01\x02\x03')

if __name__ == '__main__':
    unittest.main()