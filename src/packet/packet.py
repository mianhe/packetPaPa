import sys
sys.path.append(sys.path[0][:-11])

from bitsmap import Bitsmap
from src.log import log  
from src.converter import to_printable

class Packet():
            
    def __init__(self):
        self.__fields = []
        self._paser = Parser()
        
    def append_field(self, field):
        self.__fields.append(field)
        return self
        
    def get_value(self, name):
        field = self._get_field(name)
        if field != None:
            return field.value()

    def set_value(self, name, value):
        self._get_field(name).set_value(value)

    def pack(self):
        bitsmap = Bitsmap()
        position = 1
        for each_field in self.__fields:
            position = each_field.pack(bitsmap, position)
        return bitsmap.to_byte_stream()

    def parse(self, bit_str):
        self._paser.parse(self.__fields,bit_str);
        
    def resume_parse(self):
        self._paser.resume_parse()
    
    def _get_field(self, name):
        for each_field in self.__fields:
            if (each_field.name() == name):
                return each_field
            
    def __str__(self):
        result = 'packet start' + chr(13)+chr(10)
        for each_field in self.__fields:
            result +=  str(each_field) +  chr(13)+chr(10)
        return result + 'packet complete'

class Parser():
    def __init__(self):
        self._log = log

    def parse(self,fields,bit_str=''):
        self._bitsmap_to_be_pasrsed = Bitsmap(bit_str)
        self._fields = fields
        self._bitsmap_position_to_start_parse = 1
        self._field_nr_to_start_parse = 0
        
        self.resume_parse()

    def resume_parse(self):
        for each_field in self._fields[self._field_nr_to_start_parse:]:
            self._bitsmap_position_to_start_parse = \
                each_field.parse(self._bitsmap_to_be_pasrsed, self._bitsmap_position_to_start_parse)        
            self._field_nr_to_start_parse += 1
            self._log("the field: %s parsed, the value is: %s" % (each_field._name, to_printable(each_field._value)))
        
####################################################################################
import unittest
from mock import Mock, call 
from src.packet.fields.bits import BitsField 
from src.packet.fields.dotSplit import DotSplitField
from src.log import open_log, close_log


class TestBitsValueField(unittest.TestCase):
    packet = None
    def setUp(self):
        self.packet = Packet()
    
    def test_compose_single_bitsfield(self):
        field = BitsField('1-3', 3, 0b001)
        self.assertEqual(self.packet.append_field(field).pack(), '\x20')
        
    def test_compose_two_bitsfield_within_two_byte(self):
        field1 = BitsField('1-7', 7, 0b0000001)
        field2 = BitsField('8-10', 3, 0b010)
        self.assertEqual(self.packet \
                         .append_field(field1)\
                         .append_field(field2).pack(),'\x02\x80')

    def test_get_value(self):
        field1 = BitsField('1-7', 7, 0b0000001)
        field2 = BitsField('8-10', 3, 0b010)
        self.packet.append_field(field1).append_field(field2)
        self.assertEqual(self.packet.get_value('8-10'), 2)
        self.assertEqual(self.packet.get_value('no exist'), None)
        
    def test_set_value(self):
        field1 = BitsField('1-7', 7)
        field2 = BitsField('8-10', 3)
        self.packet.append_field(field1).append_field(field2)
        
        self.packet.set_value('1-7', 3)
        self.packet.set_value('8-10', 5)
        
        self.assertEqual(self.packet.get_value('1-7'), 3)
        self.assertEqual(self.packet.get_value('8-10'), 5)
        
    def test_parse_single_bitsfield(self):
        field1 = BitsField('1-3', 3)
        field2 = BitsField('4-6', 3)
        open_log()
        self.packet._paser._log = Mock()
        self.packet.append_field(field1).append_field(field2).parse('\x2f')
        calls = [call("the field: 1-3 parsed, the value is: 1"),\
                 call("the field: 4-6 parsed, the value is: 3")]
        self.packet._paser._log.assert_has_calls(calls, False)
        self.assertEqual(self.packet.get_value('1-3') , 0b001)
        self.assertEqual(self.packet.get_value('4-6'), 0b011)
        close_log()
        
    def test_parse_after_add_field(self):
        field1 = BitsField('1-3', 3)
        field2 = BitsField('4-6', 3)
        self.packet.append_field(field1).append_field(field2).parse('\x2f')
                    
        self.assertEqual(self.packet.get_value('1-3') , 0b001)
        self.assertEqual(self.packet.get_value('4-6'), 0b011)
        
        field3 = BitsField('7-8', 2)    
        self.packet.append_field(field3).resume_parse()
        self.assertEqual(self.packet.get_value('7-8'), 0b011)

    def test_parse_two_bitsmap_within_two_byte(self):
        field1 = BitsField('1-7', 7)
        field2 = BitsField('8-10', 3)
        self.packet.append_field(field1).append_field(field2).parse('\x02\x80')
                    
        self.assertEqual(self.packet.get_value('1-7'), 0b0000001)
        self.assertEqual(self.packet.get_value('8-10'), 0b010)
    
class TestBytesStreamField(unittest.TestCase):
    def setUp(self):
        self.packet = Packet()
        
    def test_parse_URL(self):
        temp_field = DotSplitField('default','www.123.com')
        bit_str = Packet().append_field(temp_field).pack()
        
        field1 = DotSplitField('URL')
        self.packet.append_field(field1).parse(bit_str)
        
        self.assertEqual(self.packet.get_value('URL'),\
                         'www.123.com')

    def test_parse_URL_with_bits_on_each_side(self):
        
        temp_field = DotSplitField('default','www.123.com')
        bit_str = Packet().append_field(temp_field).pack()
        
        head_field = BitsField('head', 8)
        body_field = DotSplitField('URL')
        tail_field = BitsField('tail', 8)

        self.packet.append_field(head_field)\
                   .append_field(body_field)\
                   .append_field(tail_field)\
                   .parse('\xaa'+bit_str+'\xbb')

        self.assertEqual(self.packet.get_value('URL'),'www.123.com')
        self.assertEqual(self.packet.get_value('head'),0xaa)
        self.assertEqual(self.packet.get_value('tail'),0xbb)
        
if __name__ == '__main__':
    unittest.main()