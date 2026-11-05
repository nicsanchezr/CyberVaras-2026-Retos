#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera ftp.pcap: canal de control FTP (21) + canal de datos (PASV) que
transfiere un archivo con la flag. tshark/Wireshark 'export FTP-DATA'."""
import os
from scapy.all import IP, TCP, Raw, wrpcap
HERE = os.path.dirname(os.path.abspath(__file__))
flag = open(os.path.join(HERE, "..", "flag.txt")).read().strip()

cli, srv = "10.10.10.9", "10.10.10.2"
pkts = []

def stream(sp, dp, src, dst, exchanges):
    """exchanges: lista de ('c'|'s', bytes)"""
    cseq, sseq = 100, 700
    pkts.append(IP(src=src,dst=dst)/TCP(sport=sp,dport=dp,flags="S",seq=cseq)); cseq+=1
    pkts.append(IP(src=dst,dst=src)/TCP(sport=dp,dport=sp,flags="SA",seq=sseq,ack=cseq)); sseq+=1
    pkts.append(IP(src=src,dst=dst)/TCP(sport=sp,dport=dp,flags="A",seq=cseq,ack=sseq))
    for who, data in exchanges:
        if who == 'c':
            pkts.append(IP(src=src,dst=dst)/TCP(sport=sp,dport=dp,flags="PA",seq=cseq,ack=sseq)/Raw(load=data)); cseq+=len(data)
        else:
            pkts.append(IP(src=dst,dst=src)/TCP(sport=dp,dport=sp,flags="PA",seq=sseq,ack=cseq)/Raw(load=data)); sseq+=len(data)

# PASV negocia puerto de datos 20100 (192,168 -> aqui 10.10.10.2 => 10,10,10,2,78,132)
data_port = 20100
p1, p2 = data_port >> 8, data_port & 0xFF
control = [
 ('s', b"220 CyberVaras FTP listo\r\n"),
 ('c', b"USER anonimo\r\n"), ('s', b"331 Clave requerida\r\n"),
 ('c', b"PASS correo@duocuc.cl\r\n"), ('s', b"230 Acceso concedido\r\n"),
 ('c', b"TYPE I\r\n"), ('s', b"200 Modo binario\r\n"),
 ('c', b"PASV\r\n"), ('s', f"227 Entering Passive Mode (10,10,10,2,{p1},{p2})\r\n".encode()),
 ('c', b"RETR secreto.txt\r\n"), ('s', b"150 Abriendo conexion de datos\r\n"),
 ('s', b"226 Transferencia completa\r\n"),
]
stream(40200, 21, cli, srv, control)

# canal de datos: el servidor envia el archivo
file_content = (f"# secreto.txt\n{flag}\n").encode()
stream(40201, data_port, cli, srv, [('s', file_content)])

wrpcap(os.path.join(HERE, "ftp.pcap"), pkts)
print(f"[ok] ftp.pcap generado ({len(pkts)} paquetes) — flag en canal de datos :{data_port}")
