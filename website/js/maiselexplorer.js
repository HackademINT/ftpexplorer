var serverPort = 9999;

var ftp_servers_sockets = [];

ftp_servers.push("127.0.0.1"); // On ajoute le serveur en local pour les tests.


function clearFileList() {
    var champ = document.getElementById("me_fichiers")
    champ.innerHTML = ""
}

function addFileToList(file, server) {
    var champ = document.getElementById("me_fichiers")
    
    var code = ""
    code += "<tr><td>";
    code += file[0]; // Nom de fichier
    code += "</td><td>";
    var date = new Date( file[2] * 1000 )
    code += date.getDay() + "/" + (date.getMonth()+1) + "/" + date.getFullYear(); // Date
    code += "</td><td>";
    code += server; // Localisation
    code += "</td><td>";
    code += "???"; // Catégorie
    code += "</td><td>";
    code += file[1]+"B"; // Taille
    code += "</td><td>";
    code += "<button type='button' class='btn btn-primary'>Télécharger</button>"; // Bouton
    code += "</td></tr>";
    
    champ.innerHTML += code;

}

// On cree une socket pour se connecter aux serveurs
for(i=0; i<ftp_servers.length; i++) {

    var curServ = ftp_servers[i];
    var socket = io.connect('http://' + curServ + ':' + serverPort  + '/me');
    ftp_servers_sockets.push(socket);
    socket.on("connect", function() { 

        // Quand on est connecte au serveur, on envoie une requete pour les
        // fichiers
        console.log("Connected to the server " + curServ);
        socket.emit("me_getFiles", function( data ) {
            
            console.log("Got a response !");
            
            var files = JSON.parse(data);
            clearFileList();
            for( var i in files ) {
                addFileToList( files[i], curServ);           
            }
            
        });

    });
}

document.getElementById("me_recherche").onsubmit = function() {
    for(i=0; i<ftp_servers.length; i++) {
        var socket = ftp_servers_sockets[i]; 
        socket.emit("me_search", document.getElementById("me_recherche_champ").value, function( data ) {
                
            console.log("Got a response !");
            var files = JSON.parse(data);
            clearFileList();
            for( var i in files ) {
                addFileToList( files[i], curServ ); 
            }
        });
    }
    return false;
};

