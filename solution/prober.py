#!/usr/bin/python

from time import * 
from scapy.all import *
from threading import Thread, Event
from struct import pack,unpack

class Sniffer(Thread):
    def  __init__(self, interface="eth1"):
        Thread.__init__(self)
        super(Thread,self).__init__()

        self.daemon = True

        self.socket = None
        self.interface = interface
        self.stop_sniffer = Event()

    def run(self):
        self.socket = conf.L2listen(
            type=ETH_P_ALL,
            iface=self.interface,
            filter="udp and (port 32769 or port 32768 or port 40000)",
        )

        sniff(
            opened_socket=self.socket,
            prn=self.print_packet,
            stop_filter=self.should_stop_sniffer,
            stop=0
        )
    def join(self, timeout=None):
        self.stop_sniffer.set()
        super().join(timeout)

    def should_stop_sniffer(self, packet):
        return self.stop_sniffer.isSet()

    def print_packet(self, packet):
        ip_layer = packet.getlayer(IP)
        udp_layer = packet.getlayer(UDP)
        print("[!] New Packet: {src} -> {dst}".format(src=ip_layer.src, dst=ip_layer.dst))
        sendTime,seq=unpack('dQ',packet.load)
        print ("Seq#: %.0f, SendTime: %.0f, ReceiveTime %.0f, RTT: %.0f, Port: %.0f " %(seq, sendTime*1000,packet.time*1000,(packet.time*1000-sendTime*1000),udp_layer.dport))

#Start Sniffer
sniffer = Sniffer()
print("[*] Start sniffing...")
sniffer.start()

sleep(2)

#Send packets
for i in range(1):
  p1=IP(src='20.0.0.2',proto=47,tos=0,dst='20.0.0.1',version=4,ttl=64)
  p2=GRE()
  p3=IP(src='20.0.0.2',proto=47,tos=0,dst='10.1.1.1',version=4,ttl=64)
  p4=GRE()
  p5=IP(src='20.0.0.2',proto=17,tos=0,dst='20.0.0.2',version=4,ttl=64)
  p6=UDP(dport=32768, sport=32768)
  p7=pack('dQ',time.time(),i)
  packet=p1/p2/p3/p4/p5/p6/p7
  send(packet)
  packet

for i in range(1):
  p1=IP(src='20.0.0.2',proto=47,tos=0,dst='20.0.0.1',version=4,ttl=64)
  p2=GRE()
  p3=IP(src='20.0.0.2',proto=47,tos=0,dst='10.1.1.3',version=4,ttl=64)
  p4=GRE()
  p5=IP(src='20.0.0.2',proto=17,tos=0,dst='20.0.0.2',version=4,ttl=64)
  p6=UDP(dport=32769, sport=32769)
  p7=pack('dQ',time.time(),i)
  packet=p1/p2/p3/p4/p5/p6/p7
  send(packet)
  packet

for i in range(1):
  p1=IP(src='20.0.0.2',proto=47,tos=0,dst='20.0.0.1',version=4,ttl=64)
  p2=GRE()
  p3=IP(src='20.0.0.2',proto=47,tos=0,dst='10.1.1.1',version=4,ttl=64)
  p4=GRE()
  p5=IP(src='20.0.0.2',proto=47,tos=0,dst='10.1.1.7',version=4,ttl=64)
  p6=GRE()
  p7=IP(src='20.0.0.2',proto=47,tos=0,dst='10.1.1.10',version=4,ttl=64)
  p8=GRE()
  p9=IP(src='20.0.0.2',proto=47,tos=0,dst='10.1.1.2',version=4,ttl=64)
  p10=GRE()
  p11=IP(src='20.0.0.2',proto=17,tos=0,dst='20.0.0.2',version=4,ttl=64)
  p12=UDP(dport=40000, sport=40000)
  p13=pack('dQ',time.time(),i)
  packet=p1/p2/p3/p4/p5/p6/p7/p8/p9/p10/p11/p12/p13
  send(packet)
  packet

try:
    while True:
        sleep(100)
except KeyboardInterrupt:
    print("[*] Stop sniffing")
    sniffer.join(2.0)

    if sniffer.isAlive():
        sniffer.socket.close()
