#!/usr/bin/env python3

"""
 Ceci est le script qui sera execute sur les serveurs FTP.

 ROLES:
 - Repondre aux requetes emises par le javascript executes sur le navigateur
 des clients. Le client pourra faire des recherches ou filtrer les fichiers

 MODULES EXTERNES:
 - python-socketio

"""

import socketio
import eventlet
import os,sys
import json
import threading
import time

# Port sur lequel le serveur ecoutera. Si vous modifiez cette variable, pensez
# a la modifier aussi dans le javascript du client.
APP_PORT = 9999
SCAN_TIME = 10 # Toutes les SCAN_TIME secondes, le serveur explorera les fichiers en local

class RemoteMEServer:

    """
    Cette classe represente le serveur tournant sur les machines herbergeant
    un serveur FTP.
    """

    def __init__( self, port, ftpPath ):
        """
        Constructeur
        """
        self.port = port
        self.ftpPath = ftpPath
        self.explore()

    def explore( self ):
        """
        Cette fonction permet de referencer tous les fichiers sur le ftp en les
        mettant dans une table et en construisant un arbre avec leur chemin
        """
        self.fileList = []
        self.fileTree = self._exploreRecursive( self.ftpPath )


    def _exploreRecursive( self, path ):
        """
        Methode privee, recursive permettant de construire l'arbre et de
        chercher tous les fichiers
        """

        files = []
        directories = {}
        for element in os.scandir(repr(path)[1:-1]): # On escape les caracteres
            if element.is_file():
                stats = os.stat(path + "/" + element.name)
                self.fileList += [ (element.name, stats.st_size, stats.st_mtime) ]
                files += [element.name]
            else:
                directories[element.name] = self._exploreRecursive( path + "/" + element.name)
        return [directories, files]

    def run( self ):

        """
        Creation d'un serveur capable de gerer les connexions socket.io
        effectues par le client
        """

        sio = socketio.Server()
        app = socketio.Middleware(sio)

        # Fonction de callback executees lors des events du serveur
        @sio.on('disconnect', namespace='/me')
        def disconnect_handler(client):
            print( str(client) + " was disconnected.")

        # On log les connexions
        @sio.on('connect', namespace='/me')
        def connect_handler(client, environ):
            print( str(client) + " connected." )

        @sio.on("me_getFiles", namespace="/me")
        def getfiles_handler( client ):
            # On limite temporairement a 100 le nb de fichiers envoyes
            fl = json.dumps( self.fileList[:100] )
            print( str(client) + " requested the list of the files. (" + str(min(len(self.fileList),100)) + "/"+str(len(self.fileList))+" files, "+str(len(fl))+"B)")
            return fl # On renvoie en JSON la liste des fichiers+leurs attributs

        @sio.on("me_search", namespace="/me")
        def search_handler( client, text):
            print( str(client) + " searched " + text)
            result = []
            for f in self.fileList:
                if f[0].find(text) != -1:
                    result += [f]
            return json.dumps( result[:100] )

        # On lance le serveur
        eventlet.wsgi.server(eventlet.listen(('', self.port)), app)

class ThreadMEServer( threading.Thread ):
    """
    Thread qui permet d'herberger le serveur ME
    """

    def __init__(self, serv):
        """
        Constructeur
        """
        self.server = serv
        threading.Thread.__init__(self) # Initialisation du thread

    def run(self):
        """
        Lance le serveur pendant le thread
        """
        print("[SERVER] Running the server")
        self.server.run()

class ThreadMEScan( threading.Thread ):
    """
    Thread qui permet de scanner les fichiers en local
    """

    def __init__(self, serv):
        """
        Constructeur
        """
        self.shouldRun = True
        self.server = serv
        threading.Thread.__init__(self) # Initialisation du thread

    def run(self):
        """
        Force l'actualisation des fichiers
        """
        while self.shouldRun:
            print("[SCAN] Exploring...")
            self.server.explore()
            time.sleep( SCAN_TIME )

    def stop(self):
        self.shouldRun = False

if __name__ == "__main__":

    path = ""
    if len(sys.argv) > 1:
        path = sys.argv[1]
    else:
        print("Missing argument, you must specify the path of the folder containing the FTP files")
        exit()

    server = RemoteMEServer( APP_PORT, path )
    threadMEServer = ThreadMEServer( server )
    threadMEScan = ThreadMEScan( server )

    threadMEServer.start()
    threadMEScan.start()

    threadMEServer.join() # On attend la fin du serveur

    threadMEScan.stop()
    threadMEScan.join()

