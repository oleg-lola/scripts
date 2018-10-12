#!/usr/bin/env python
"""
Very simple HTTP server in python.
Usage::
    ./dummy-web-server.py [<port>]
Send a GET request::
    curl http://localhost
Send a HEAD request::
    curl -I http://localhost
Send a POST request::
    curl -d "foo=bar&bin=baz" http://localhost
"""
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from os import curdir, sep
import SocketServer
import requests, json
import redis
r = redis.StrictRedis(host='redis', port=6379, db=0)
r.set('get_count', 0)
r.set('post_count', 0)

class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Keep-Alive', 'timeout=5')
        self.send_header('Server', 'Not your fkn bussines')
        self.end_headers()

    def do_GET(self):
        if self.path=="/":
            self.path="/main.html"
        try:
            sendReply = True
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
                quote = get_quotes()
                r.incr('get_count')
                get_num = r.get('get_count')
                post_num = r.get('post_count')
                fib_num = fib(int(post_num))
                content = f.format(get_num, post_num, fib_num, quote)
                self.send_response(200)
                self.send_header('Content-type', mimetype)
                self.send_header('Keep-Alive', 'timeout=5')
                self.send_header('Server', 'Not your fkn bussines')
                self.end_headers()
                self.wfile.write(content)
                procfile.close()
            return
        except IOError:
            self.send_error(404,'File Not Found: %s' % self.path)

    def do_HEAD(self):
        self._set_headers()
        self.wfile.write("Stop doing this")

    def do_POST(self):
        self._set_headers()
        r.incr('post_count')
        get_num = r.get('get_count')
        post_num = r.get('post_count')
        fib_num = fib(int(post_num))
        data = get_content()
        content = data.format(get_num, post_num, fib_num, "wise quote here")
        self.wfile.write(content)

def fib(index):
    if index < 2:
        return 1
    else:
        num = fib(int(index) - 1) + fib(int(index) - 2)
    return num

def get_content():
    with open('appy/main.html', 'r') as myfile:
            data = myfile.read().replace('\n', '')
    return data

def get_quotes():
    #link = "http://quotesondesign.com/wp-json/posts?filter[orderby]=rand&filter[posts_per_page]=1"
    link = "http://quotesondesign.com/api/3.0/api-3.0.json"
    quote = requests.get(link).json()['quote']
    return quote

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
