var serverPort = 9999;

//alert(ftp_servers);

ftp_servers.push("127.0.0.1"); // On ajoute le serveur en local pour les tests.

// On cree une socket pour se connecter aux serveurs
for(i=0; i<ftp_servers.length; i++) {

    var curServ = ftp_servers[i];
    var socket = io.connect('http://' + curServ + ':' + serverPort  + '/me');
    socket.on("connect", function() { 

        // Quand on est connecte au serveur, on envoie une requete pour les
        // fichiers
        console.log("Connected to the server " + curServ);
        socket.emit("me_getFiles", function( data ) {
            
            // On quitte apres avoir recu la reponse
            console.log("Got a response !");
            
            var files = JSON.parse(data);
            var champ = document.getElementById("me_fichiers")
            champ.innerHTML = ""
            for( var i in files ) {
                var code = ""
                code += "<tr><td>";
                code += files[i][0]; // Nom de fichier
                code += "</td><td>";
                var date = new Date( files[i][2] * 1000 )

                code += date.getDay() + "/" + (date.getMonth()+1) + "/" + date.getFullYear(); // Date
                code += "</td><td>";
                code += curServ; // Localisation
                code += "</td><td>";
                code += "???"; // Catégorie
                code += "</td><td>";
                code += files[i][1]+"B"; // Taille
                code += "</td><td>";
                code += "<button type='button' class='btn btn-primary'>Télécharger</button>"; // Bouton
                code += "</td></tr>";
                champ.innerHTML += code;
           
            }
            console.log(champ.innerHTML);
            
            socket.disconnect();
        });

    });
}
