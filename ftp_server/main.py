#!/usr/bin/env python3

import socketio
import eventlet
import os
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
        self.fileList = []
        self.fileTree = self._exploreRecursive( self.ftpPath )

    def _exploreRecursive( self, path ):
        files = []
        directories = {}
        for element in os.scandir(path):
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
            print( str(client) + " requested the list of the files.")
            print(json.dumps(self.fileList))
            return json.dumps( self.fileList )
            #return "Ce bout de texte est téléchargé par le client grâce à un bout de javascript qui va faire une requête au serveur géré en python."

        eventlet.wsgi.server(eventlet.listen(('', self.port)), app)

if __name__ == "__main__":
    server = RemoteMEServer( 9999, "/tmp/ftp" )
    server.run()
