#!/usr/bin/env python3

import socketio
import eventlet
import os,sys
import json

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

        @sio.on('connect', namespace='/me')
        def connect_handler(client, environ):
            print( str(client) + " connected." )

        @sio.on("me_getFiles", namespace="/me")
        def getfiles_handler( client ):
            fl = json.dumps( self.fileList[:100] ) # On limite temporairement a 100 le nb de fichiers envoyes
            print( str(client) + " requested the list of the files. (100/"+str(len(self.fileList))+" files, "+str(len(fl))+"B)")
            return fl

        @sio.on("me_search", namespace="/me")
        def search_handler( client, text):
            print( str(client) + " searched " + text)
            result = []
            for f in self.fileList:
                if f[0].find(text) != -1:
                    result += [f]
            return json.dumps( result[:100] )

        eventlet.wsgi.server(eventlet.listen(('', self.port)), app)

if __name__ == "__main__":
    path = ""
    if len(sys.argv) > 1:
        path = sys.argv[1]
    else:
        print("Missing argument, you must specify the path of the folder containing the FTP files")
        exit()
    server = RemoteMEServer( 9999, "/tmp/ftp" )
    server.run()
