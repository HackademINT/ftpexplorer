#!/usr/bin/env python

"""
Ceci est le script qui sera execute sur
le serveur ME.
"""
from ftpscanner import *
from bottle import route, run, static_file, template
import bottle


scanner = FTPScanner("157.159.41-49.0/24")
addressStr = ''
scan = scanner.scan()
for i in range(len(scan)):
    addr = scan[i]
    if i != 0:
        addressStr += ","
    addressStr += "\"" + addr + "\""


print(addressStr)
bottle.TEMPLATE_PATH += ["../website"]

@route('/<filepath:path>')
def server_static(filepath):
        return static_file(filepath, root='../website/')
@route("/")
def server_temp():
    return template("index", ftpserv=addressStr)
run(host="localhost", port=8080, debug=True)
