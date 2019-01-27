#!/usr/bin/env python
"""
NOTE!
Base taken from Github gist: https://gist.github.com/bradmontgomery/2219997

This module is used to test HINT outgoing requests (as if they were sent
to a HUME).
"""

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
import json

from http.server import BaseHTTPRequestHandler, HTTPServer


class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._set_headers()

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        # Get data to see what was sent
        body_data = self.rfile.read(int(self.headers['Content-Length']))
        print("POST data: {}".format(json.loads(body_data)))

        self._set_headers()


def run(server_class=HTTPServer, handler_class=S, port=80):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print('Starting server...')
    httpd.serve_forever()


if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
