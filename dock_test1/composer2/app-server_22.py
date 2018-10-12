#!/usr/bin/env python
"""
Very simple HTTP server in python.
Usage::
    ./dummy-web-server.py [<port>]

version: 2.0
"""
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from os import curdir, sep
import SocketServer
import requests, json, hashlib, socket, os, redis
get_num = 0
post_num = 0
#REDIS_HOST = os.environ['REDIS_HOST']
REDIS_HOST = '127.0.0.1'
WORKER_HOST = '127.0.0.1'
r = redis.StrictRedis(host=REDIS_HOST, port=6379, db=0)

class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Server', 'Not your fkn bussines')
        self.end_headers()

    def do_GET(self):
        if self.path=="/":
            self.path="/index.html"
        try:
            sendReply = False
            if self.path.endswith(".html"):
                mimetype='text/html'
                sendReply = True
            if self.path.endswith(".jpg"):
                mimetype='image/jpg'
                sendReply = True
            if self.path.endswith(".gif"):
                mimetype='image/gif'
                sendReply = True
            if self.path.endswith(".js"):
                mimetype='application/javascript'
                sendReply = True
            if self.path.endswith(".css"):
                mimetype='text/css'
                sendReply = True

            if sendReply == True:
                procfile = open(curdir + sep + 'appy' + self.path, 'r')
                f = procfile.read().replace('\n', '')
                global get_num
                get_num += 1
                str = ("get,{},").format(get_num)
                quote = get_quotes()
                #hasher(quote)
                if socksend(str) == False:
                    print "Socket fucked up"
                    exit
                if self.path == "/main.html":
                    g_num, g_fib, p_num, p_fib = get_cache()
                    #print (g_num, p_num, g_fib, p_fib)
                    content = f.format(g_num, p_num, g_fib, p_fib, quote)
                elif self.path == "/index.html":
                    g_num, g_fib, p_num, p_fib = get_cache()
                    #print (g_num, p_num, g_fib, p_fib)
                    content = f.format(g_num, p_num, quote)
                else:
                    content = f
                self.send_response(200)
                self.send_header('Content-type', mimetype)
                self.end_headers()
                self.wfile.write(content)
                procfile.close()
            else:
                procfile = open(curdir + sep + 'appy' + self.path, 'r')
                f = procfile.read()
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(f)
                procfile.close()
            return
        except IOError:
            self.send_error(404,'File Not Found: %s' % self.path)

    def do_HEAD(self):
        self._set_headers()
        self.wfile.write("Stop doing this")

    def do_POST(self):
        global post_num
        post_num += 1
        #string = "post" + "," + post_num
        socksend('post' + "," + post_num)
        get_num = get_cache()
        get_fib = get_cache()
        #post_num = get_cache()
        post_fib = get_cache()
        #fib_num = fib(int(post_num))
        data = get_content()
        content = data.format(get_num, post_num, fib_num, "wise quote here")
        self._set_headers()
        self.wfile.write(content)
"""
def fib(index):
    if index < 2:
        return 1
    else:
        num = fib(int(index) - 1) + fib(int(index) - 2)
    return num
"""

def socksend(comm):
    global WORKER_HOST
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
    try:
        s.connect((WORKER_HOST, int(9999)))
        s.send(comm)
        s.shutdown(socket.SHUT_RDWR)
        return True
    except:
        return False
        s.close()

def get_content():
    with open('appy/main.html', 'r') as myfile:
            data = myfile.read().replace('\n', '')
    return data

def get_cache():
    global r
    get_num = r.get('get_num')
    get_fib = r.get('get_fib')
    post_num = r.get('post_num')
    post_fib = r.get('post_fib')
    return get_num, get_fib, post_num, post_fib

def get_quotes():
    #link = "http://quotesondesign.com/wp-json/posts?filter[orderby]=rand&filter[posts_per_page]=1"
    link = "http://quotesondesign.com/api/3.0/api-3.0.json"
    quote = requests.get(link).json()['quote']
    return quote

def hasher(str):
    hash_object = hashlib.sha1(b'str')
    hex_dig = hash_object.hexdigest()
    print(hex_dig)
    return hex_dig

def run(server_class=HTTPServer, handler_class=S, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print 'Starting httpd...'
    httpd.serve_forever()


if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
