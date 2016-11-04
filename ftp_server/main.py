import socketio
import eventlet

class RemoteMEServer:

    """
    Cette classe represente le serveur tournant sur les machines herbergeant
    un serveur FTP.
    """

    def __init__( self, port ):
        """
        Constructeur
        """
        self.port = port

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
            return "Ce bout de texte est téléchargé par le client grâce à un bout de javascript qui va faire une requête au serveur géré en python."

        eventlet.wsgi.server(eventlet.listen(('', self.port)), app)


server = RemoteMEServer( 9999 )
server.run()
