#!/usr/bin/env python

"""
Ceci est le script qui sera execute sur
le serveur ME.
"""
from ftpscanner import *
from bottle import route, run, static_file, template
import bottle

print("Scanning the network...")
scanner = FTPScanner("157.159.41-49.0/24")
addressStr = ''
#scan = scanner.scan()
scan = []
print("FTP servers online:")
for i in range(len(scan)):
    addr = scan[i]
    print(" - " + addr)
    if i != 0:
        addressStr += ","
    addressStr += "\"" + addr + "\""


bottle.TEMPLATE_PATH += ["../website"]

@route('/<filepath:path>')
def server_static(filepath):
        return static_file(filepath, root='../website/')
@route("/")
def server_temp():
    return template("index", ftpserv=addressStr)
run(host="localhost", port=8080, debug=True)
