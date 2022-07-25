import logging
import os
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import BaseRequestHandler, ThreadingMixIn
from typing import Callable, Any, Tuple
from concurrent.futures import ThreadPoolExecutor


def run(server_class=HTTPServer, handler_class=BaseHTTPRequestHandler):
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


class MyRequestHandler(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        self._set_response()
        time.sleep(10)
        output = ''
        try:
            for d in os.listdir('.' + self.path):
                path = self.path + ('/' if self.path[-1] != '/' else '')
                if os.path.isdir(f'.{path}{d}'):
                    output += f'<a href = "{path}{d}"><li>{d}</li></a>'
                else:
                    output += f'{d}<br>'
        except Exception as e:
            output = str(e)

        self.wfile.write(output.encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])  # <--- Gets the size of data
        post_data = self.rfile.read(content_length)  # <--- Gets the data itself
        logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                     str(self.path), str(self.headers), post_data.decode('utf-8'))

        self._set_response()
        self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))


class ThreadingSimpleServer(ThreadingMixIn, HTTPServer):
    pass

if __name__ == '__main__':
    run(server_class=ThreadingSimpleServer, handler_class=MyRequestHandler)
