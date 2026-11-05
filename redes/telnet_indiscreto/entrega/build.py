#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera telnet.pcap: sesion Telnet (puerto 23) en texto claro donde el usuario
teclea un comando que imprime la flag. Follow TCP Stream lo reconstruye."""
import os
from scapy.all import IP, TCP, Raw, wrpcap
HERE = os.path.dirname(os.path.abspath(__file__))
flag = open(os.path.join(HERE, "..", "flag.txt")).read().strip()

cli, srv = "172.16.5.22", "172.16.5.1"
sp, dp = 44120, 23
cseq, sseq = 2000, 9000
pkts = []
pkts.append(IP(src=cli,dst=srv)/TCP(sport=sp,dport=dp,flags="S",seq=cseq)); cseq+=1
pkts.append(IP(src=srv,dst=cli)/TCP(sport=dp,dport=sp,flags="SA",seq=sseq,ack=cseq)); sseq+=1
pkts.append(IP(src=cli,dst=srv)/TCP(sport=sp,dport=dp,flags="A",seq=cseq,ack=sseq))

def c2s(p):
    global cseq
    pkts.append(IP(src=cli,dst=srv)/TCP(sport=sp,dport=dp,flags="PA",seq=cseq,ack=sseq)/Raw(load=p)); cseq+=len(p)
def s2c(p):
    global sseq
    pkts.append(IP(src=srv,dst=cli)/TCP(sport=dp,dport=sp,flags="PA",seq=sseq,ack=cseq)/Raw(load=p)); sseq+=len(p)

s2c(b"Ubuntu 20.04 LTS\r\nlogin: ")
for ch in b"operador": c2s(bytes([ch])); s2c(bytes([ch]))   # eco char por char
c2s(b"\r\n"); s2c(b"\r\nPassword: ")
c2s(b"\r\n")
s2c(b"\r\n$ ")
cmd = f"echo {flag}".encode()
for ch in cmd: c2s(bytes([ch])); s2c(bytes([ch]))
c2s(b"\r\n"); s2c(b"\r\n" + flag.encode() + b"\r\n$ ")

wrpcap(os.path.join(HERE, "telnet.pcap"), pkts)
print(f"[ok] telnet.pcap generado ({len(pkts)} paquetes)")
