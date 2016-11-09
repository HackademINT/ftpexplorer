/*
 * Ce script sera execute sur les clients apres qu'ils aient teleche la page
 * sur me.minet.net. Il a pour role de completer la page en allant chercher
 * les informations sur les fichiers presents sur les serveurs FTP 
 */


var serverPort = 9999; // Port sur lequel tourne le script python de ftp_server
var ftp_servers_sockets = []; // On stocke les sockets ouvertes

// TODO: supprimer cette ligne
ftp_servers.push("127.0.0.1"); // On ajoute le serveur en local pour les tests.


function clearFileList() {
    /*
     * Vide la liste des fichiers
     */
    var champ = document.getElementById("me_fichiers")
    champ.innerHTML = ""
}

function addFileToList(file, server) {
    /*
     * Ajoute une ligne a la liste des fichiers
     * Prend en argument un tableau sous le format : [nom, taille, date]
     * Prend en argument l'ip du serveur de provenance
     */

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
            
            // On affiche tous les fichiers du FTP
            var files = JSON.parse(data);
            clearFileList();
            for( var i in files ) {
                addFileToList( files[i], curServ);           
            }
            
        });

    });
}


document.getElementById("me_recherche").onsubmit = function() {
    /*
     * Execute lorsque l'utilisateur fait une recherche
     */

    // On envoie une requete a chaque serveur
    for(i=0; i<ftp_servers.length; i++) {

        var socket = ftp_servers_sockets[i]; 
        // On envoie au serveur le mot recherche
        socket.emit("me_search", document.getElementById("me_recherche_champ").value, function( data ) {
                
            console.log("Got a response !");

            // Et on complete la liste...
            var files = JSON.parse(data);
            clearFileList();
            for( var i in files ) {
                addFileToList( files[i], curServ ); 
            }

        });
    }
    return false; // Empeche la page de se rafraichir apres la recherche
};

