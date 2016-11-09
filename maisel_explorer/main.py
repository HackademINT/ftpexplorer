#!/usr/bin/env python

"""
Ceci est le script qui sera execute sur le serveur ME.

ROLES:
- Scanner le reseau pour detecter les serveurs FTP
- Faire un serveur web pour que les clients puissent recuperer une page
contenant un script JS et les differentes ip des serveurs FTP

MODULES EXTERNES:
- Bottle
- Python-nmap

"""

from bottle import route, run, static_file, template
import bottle
import threading
import time
from ftpscanner import *

WEBSITE_PATH = "../website"
WEBSITE_PORT = 8080
WEBSITE_HOST = "localhost"

SCAN_TIME = 10 # 10 secondes entre chaque scan

class ScanThread(threading.Thread):
    """
    Classe representant un thread qui executera un scan des serveurs FTP sur
    le reseau regulierement, en parallele du serveur web.
    """

    def __init__(self, threadWeb):
        """
        Constructeur, prend en argument le thread web pour pouvoir lui
        envoyer via une methode, la liste des serveurs FTP up.
        """
        self.shouldRun = True       # Si shouldRun = false, le thread stop
        self.threadWeb = threadWeb
        threading.Thread.__init__(self) # Initialise le thread

    def run(self):
        """
        Fonction qui sera appelee quand le thread se lancera.
        """

        while self.shouldRun:
            self.scanMiNET()
            time.sleep( SCAN_TIME )

    def scanMiNET( self ):
        """
        Fonction qui envoie au thread du serveur web les ip des serveurs FTP
        """

        print("[SCAN] Scanning the network...")
        scanner = FTPScanner("192.168.41-49.0/24")
        scan = scanner.scan()
        print("[SCAN] FTP servers up " + str(scan) )
        self.threadWeb.setFTPServer( scan )


    def stop( self ):
        """
        Ce fonction est utilisee pour arreter le thread, elle est utilisee si
        le serveur web s'arrete, alors les scans s'arretent aussi.
        """
        self.shouldRun = False

class BottleThread(threading.Thread):
    """
    Classe qui represente le thread du serveur web qui s'executera en parallele
    des scans.
    """

    def __init__(self):
        """
        Constructeur du thread, son role est d'initialiser les fonctions utiles
        pour le serveur web utilisant Bottle.
        """

        #Variable string sous forme: ip1,ip2,...,ipn qui sera envoyee dans la
        #page pour indiquer aux clients les serveurs FTP
        self.addressStr = ""

        threading.Thread.__init__(self) # Initialise le thread

        # Indique a bottle ou sont les pages statiques
        bottle.TEMPLATE_PATH += [WEBSITE_PATH]

        # Redirige les requetes HTTP vers les fichiers sur le serveur web.
        @route('/<filepath:path>')
        def server_static(filepath):
                return static_file(filepath, root=WEBSITE_PATH)

        # Si la requete est me.minet.net/ alors on renvoie la template
        # completee avec les IPs
        @route("/")
        def server_temp():
            return template("index", ftpserv=self.addressStr)

    def setFTPServer( self, scan ):
        """
        Fonction appelee par le scanner qui actualise la liste des erveurs FTP.
        """

        self.addressStr = ",".join(scan)

        # On rebind /
        @route("/")
        def server_temp():
            return template("index", ftpserv=self.addressStr)


    def run(self):
        """
        Fonction qui sera executee pendant le thread
        """
        print("[WEB] Starting the server")
        # On lance le serveur web
        run(host=WEBSITE_HOST, port=WEBSITE_PORT)#, debug=True)
        print("[WEB] Server stopped...")

if __name__ == '__main__':

    #Creation des threads
    threadWeb = BottleThread()
    threadScan = ScanThread( threadWeb )

    #Lancement des threads
    threadWeb.start()
    threadScan.start()

    #Atente de fin du serveur web
    threadWeb.join()

    print("ThreadWeb stopped, stopping ThreadScan...")
    threadScan.stop()
    threadScan.join()

