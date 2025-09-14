#!/usr/bin/env python

""" ip-tools - A simple web app to return ip/ptr/headers requester """

# Copyright 2014 Major Hayden
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import json
import os
import socket
import time

from flask import Flask, Response, request, send_from_directory

app = Flask(__name__, static_folder='static')

# Check for ENABLE_PROXY_HEADERS environment variable
ENABLE_PROXY_HEADERS = os.environ.get('ENABLE_PROXY_HEADERS', 'false')

def find_remote_addr():
    """ Determine the correct IP address of the requester """
    if request.headers.get('CF-Connecting-IP'):
        return request.headers.get('CF-Connecting-IP')
    if request.headers.get('X-Forwarded-For'):
        return request.headers.get('X-Forwarded-For')
    return request.remote_addr

@app.route('/health')
def healthcheck():
    """ Healthcheck Route"""
    return "healthy"

@app.route("/")
def main():
    """ Main Route - Determine what to return based on hostname """
    # Set default mimetype
    mimetype = "text/plain"

    # Determine remote address from request
    remote_addr = find_remote_addr()

    if request.host.startswith('ip.'):
        # The request is for ip.domain.com
        result = remote_addr
    elif request.host.startswith('epoch.'):
        # The request is for epoch.domain.com
        epoch_time = int(time.time())
        result = epoch_time
    elif request.host.startswith('headers.'):
        # The request is for headers.domain.com
        mimetype = "application/json"
        result = json.dumps(dict(request.headers))
    elif request.host.startswith('proxy-headers.') \
        and ENABLE_PROXY_HEADERS.lower() in ('true', '1', 'yes'):
        # The request is for proxy.domain.com
        proxy_headers = [
            'via',
            'forwarded',
            'client-ip',
            'useragent_via',
            'proxy_connection',
            'xproxy_connection',
            'http_pc_remote_addr',
            'http_client_ip',
            'http_x_appengine_country'
            ]
        found_headers = {}
        for header in proxy_headers:
            value = request.headers.get(header, None)
            if value:
                found_headers[header] = value.strip()
        if len(found_headers) > 0:
            mimetype = "application/json"
            result = json.dumps(found_headers)
        else:
            return Response(""), 204
    elif request.host.startswith('ptr.'):
        # The request is for ptr.domain.com
        try:
            output = socket.gethostbyaddr(remote_addr)
            result = output[0]
        except:
            result = remote_addr
    else:
        # The request is for something we don't recognize
        result = remote_addr
    return Response("%s\n" % result, mimetype=mimetype, headers={"X-Your-Ip": remote_addr})

@app.route('/robots.txt')
def static_from_root():
    """ Serve robots.txt to prevent indexing """
    return send_from_directory(app.static_folder, request.path[1:])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
