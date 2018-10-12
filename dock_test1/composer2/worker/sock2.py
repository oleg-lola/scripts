#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket

sock = socket.socket()
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('0.0.0.0', 9999))
sock.listen(1)

def new_conn(sock):
    conn, addr = sock.accept()
    conn.settimeout(60)
    while True:
        data = conn.recv(1024)
        data = data.strip()
        if not data:
            break
        print(data.upper())
    conn.close()

try:
    while True:
        new_conn(sock)
finally: sock.close()
