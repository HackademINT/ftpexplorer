var serverPort = 9999

// On cree une socket pour se connecter au serveur
var socket = io.connect('http://127.0.0.1:' + serverPort  + '/me');
socket.on("connect", function() { 

    // Quand on est connecte au serveur, on envoie une requete pour les
    // fichiers
    console.log("Connected to the server.");
    socket.emit("me_getFiles", function( data ) {
        
        // On quitte apres avoir recu la reponse
        console.log("Got a response !");
        document.getElementById("result").innerHTML = data;
        socket.disconnect();
    });

});
