#!/usr/bin/env python

import socket
import redis

REDIS_HOST = '127.0.0.1'
r = redis.StrictRedis(host=REDIS_HOST, port=6379, db=0)
r.set('get_num', 0)
r.set('post_num', 0)
r.set('get_fib', 0)
r.set('post_fib', 0)

def fib(index):
    if index < 2:
        return 1
    else:
        num = fib(int(index) - 1) + fib(int(index) - 2)
    return num

def push(comm, n):
    if comm == 'get':
        get_num = int(n)
        get_fib = fib(int(get_num))
        r.set('get_num', get_num)
        r.set('get_fib', get_fib)
    if comm == 'post':
        post_num = int(n)
        post_fib = fib(int(post_num))
        r.set('post_num', post_num)
        r.set('post_fib', post_fib)

def new_conn(sock):
    conn, addr = sock.accept()
    conn.settimeout(60)
    #print 'connected:', addr
    while True:
        data = conn.recv(1024)
        data = data.strip()
        if not data:
            break
        comm = data.split(",")[0]
        n = data.split(",")[1]
        push(comm, n)
    conn.close()

sock = socket.socket()
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('0.0.0.0', 9999))
sock.listen(1)

print ("Starting new worker process on port  9999.")
try:
    while True:
        new_conn(sock)
finally: sock.close()
