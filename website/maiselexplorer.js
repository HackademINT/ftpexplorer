var serverPort = 9999;




// On cree une socket pour se connecter au serveur
var socket = io.connect('http://127.0.0.1:' + serverPort  + '/me');
socket.on("connect", function() { 

    // Quand on est connecte au serveur, on envoie une requete pour les
    // fichiers
    console.log("Connected to the server.");
    socket.emit("me_getFiles", function( data ) {
        
        // On quitte apres avoir recu la reponse
        console.log("Got a response !");
        
        var files = JSON.parse(data);
        var champ = document.getElementById("me_fichiers")
        champ.innerHTML = ""
        for( var i in files ) {
            var code = ""
            code += "<tr><td>";
            code += files[i]; // Nom de fichier
            code += "</td><td>";
            code += "17/02/1996"; // Date
            code += "</td><td>";
            code += "127.0.0.1"; // Localisation
            code += "</td><td>";
            code += "???"; // Catégorie
            code += "</td><td>";
            code += "? GiB"; // Taille
            code += "</td><td>";
            code += "<button type='button' class='btn btn-primary'>Télécharger</button>"; // Bouton
            code += "</td></tr>";
            champ.innerHTML += code;
       
        }
        console.log(champ.innerHTML);
        
        socket.disconnect();
    });

});
