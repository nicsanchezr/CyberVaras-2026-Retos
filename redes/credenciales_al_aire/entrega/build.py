#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera captura.pcap con un POST HTTP de login (texto claro) cuyo campo
password es la flag. Follow TCP Stream / tshark http lo revelan. Requiere scapy."""
import os
from scapy.all import IP, TCP, Raw, wrpcap
HERE = os.path.dirname(os.path.abspath(__file__))
flag = open(os.path.join(HERE, "..", "flag.txt")).read().strip()

cli, srv = "10.0.0.15", "192.168.10.80"
sp, dp = 50512, 80
cseq, sseq = 1000, 5000
pkts = []
def c2s(payload, flags="PA"):
    global cseq
    p = IP(src=cli, dst=srv)/TCP(sport=sp, dport=dp, flags=flags, seq=cseq, ack=sseq)/Raw(load=payload)
    cseq += len(payload); pkts.append(p)
def s2c(payload, flags="PA"):
    global sseq
    p = IP(src=srv, dst=cli)/TCP(sport=dp, dport=sp, flags=flags, seq=sseq, ack=cseq)/Raw(load=payload)
    sseq += len(payload); pkts.append(p)

# handshake
pkts.append(IP(src=cli,dst=srv)/TCP(sport=sp,dport=dp,flags="S",seq=cseq)); cseq+=1
pkts.append(IP(src=srv,dst=cli)/TCP(sport=dp,dport=sp,flags="SA",seq=sseq,ack=cseq)); sseq+=1
pkts.append(IP(src=cli,dst=srv)/TCP(sport=sp,dport=dp,flags="A",seq=cseq,ack=sseq))

body = f"usuario=admin&password={flag}"
req = ("POST /login HTTP/1.1\r\n"
       "Host: intranet.cybervaras.local\r\n"
       "User-Agent: Mozilla/5.0\r\n"
       "Content-Type: application/x-www-form-urlencoded\r\n"
       f"Content-Length: {len(body)}\r\n"
       "\r\n" + body).encode()
c2s(req)
resp = ("HTTP/1.1 302 Found\r\nLocation: /panel\r\nContent-Length: 0\r\n\r\n").encode()
s2c(resp)

wrpcap(os.path.join(HERE, "captura.pcap"), pkts)
print(f"[ok] captura.pcap generado ({len(pkts)} paquetes) — password en POST")
