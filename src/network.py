import socket
DEFALUT_RECV_TIMEOUT = 1
DEFALUT_RECV_BUFFER_SIZE = 1000
channel_g = None

def setup_network(ip,source_port,destination_port):
    global channel_g
    channel_g = Channel(ip,source_port,destination_port) 
def close_network():
    global channel_g
    channel_g.close() 
def send_buffer(data):
    global channel_g
    channel_g.send(data) 

class Channel:
    def __init__(self, dst_ip,src_port,dst_port):
        self._dst_ip = dst_ip
        self._src_port = src_port
        self._dst_port = dst_port
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._sock.bind(('', self._src_port))

    def __del__(self):
        self._sock.close()
    def close(self):
        self.__del__()       
                                                                                    
    def send(self,data):
        self._sock.close()
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)                                                                   
        self._sock.bind(('', self._src_port))
        self._sock.sendto(data, (self._dst_ip, self._dst_port))

    def receive(self):
        self._sock.settimeout(DEFALUT_RECV_TIMEOUT)
        data = self._sock.recv(DEFALUT_RECV_BUFFER_SIZE)
        return data
#_____________________________________________

import unittest
class TestConsole(unittest.TestCase):
    def setUp(self):
        setup_network('127.0.0.1', 4001,4002)
    def tearDown(self):
        close_network()
    
    def test_send_Packet(self):
        receieve_channel = Channel('127.0.0.1', 4002,4001)
        send_buffer('abc')
        self.assertEqual(receieve_channel.receive(), 'abc')
if __name__ == '__main__':
    unittest.main()