#!/usr/bin/env python3
# coding: utf-8
# Copyright 2016 Abram Hindle, https://github.com/tywtyw2002, and https://github.com/treedust
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
# you may use urllib to encode data appropriately
import urllib.parse

def help():
    print("httpclient.py [GET/POST] [URL]\n")

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):
    #def get_host_port(self,url):

    #easily retrieve host, port and path from a given url by this function
    # so we can use this everytime we need to obtain host, port and path
    def getHostPortPath(self,url):
        host = urlparse(url).hostname
        port = urlparse(url).port
        path = urlparse(url).path
        if port != None:
            return host,port,path
        else:
            port = 80
            return host,port,path

    def connect(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        return None

    def get_code(self, data):
        response_needed = data.split("\n")
        code = int(response_needed[0].split(' ')[1])

        return code

    def get_headers(self,data):
        return data.split("\n")[0]

    def get_body(self, data):
        if data:
            try:
                body = data.split('\r\n\r\n')[1]
            except:
                raise Exception('Body not Found!')

        return body
    
    def sendall(self, data):
        self.socket.sendall(data.encode('utf-8'))
        
    def close(self):
        self.socket.close()

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return buffer.decode('utf-8')

    def GET(self, url, args=None):
        #code = 500
        #body = ""
        #first, obtain host, port, and path information from given url
        host,port,path = self.getHostPortPath(url)
        #second, connect
        self.connect(host,port)
        #third, send data
        parsed_url = urllib.parse.urlparse(url)
        # concatenate the query to path
        if (parsed_url.query != ''):
            path += "?" + parsed_url.query
        complete_command = ("GET {p1} HTTP/1.1\r\n"+"Host: {p2}\r\n"+"Accept: */*\r\n\r\n")
        final_command = complete_command.format(p1=path,p2=host)
        self.sendall(command)
        #then receive data
        recv_data = self.recvall(self.socket)
        #get code and body content
        code = self.get_code(recv_data)
        body = self.get_body(recv_data)
        #close the connection
        self.close()
        return HTTPResponse(code, body)

    def POST(self, url, args=None):
        code = 500
        body = ""
        #first, obtain host, port, and path information from given url
        host,port,path = self.getHostPortPath(url)
        self.connect(host,port)
        if args:
            self.sendall("POST {file} HTTP/1.1\r\n"  + "Host: {host}\r\n" + "Content-Length: {length2}\r\n"  + "Content-Type: {content_type}; charset=UTF-8\r\n\r\n")

        return HTTPResponse(code, body)

        #https://github.com/UAACC/CMPUT404-assignment-web-client
        #from Dongheng

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )
    
if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print(client.command( sys.argv[2], sys.argv[1] ))
    else:
        print(client.command( sys.argv[1] ))
