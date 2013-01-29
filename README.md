packetPaPa
==========

Robot Framework Library for network packet pack and parse(Packet PaPa) , as well as send and recieve the packet

- define the packet
- pack a packet according to the value given for each field 
- parse the packet recieved from the network, or input as a bytestream, according to the packet definition
- send and recieve the packet from network
 
- a couple of pre-defined prtotcol packet(e.g. dhcp, dns), more is coming
- ready to be extent at robot user key words level to support any kind of packet at L2/L3/L3+
 
 

To do List:
- to support more kinds of packet 
- to support only UDP but also TCP and STCP, and Ethernet Frames (Raw Scoket)
- to support calcualtion field (e.g. 802.1x packet)
