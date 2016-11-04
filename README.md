Projet ME
===================


Le projet **ME** consiste à développer une application pour permettre une recherche de fichiers facile parmi tous les serveurs FTP présents sur le réseau de MiNET.

Vous connaissez rien en programmation objet et en classe ?
-----------------

http://apprendre-python.com/page-apprendre-programmation-orientee-objet-poo-classes-python-cours-debutants

Comment accéder aux fichiers de **ME** ?
-------------

Pour cloner le dépôt git, créez vous un dossier, déplacez vous dedans et faites la commande : git clone http://gitlab.minet.net/thunder/me.git
> **Note**: Pensez à faire un git fetch origin pour avoir toutes les branches distantes 

Mise en place de virtualenv & des modules
-------------
**Virtualenv** est un outil pour créer un environnement python isolé. Nous installerons les modules nécessaires à notre projet dans ces environnements. Pour installer les modules et **virtualenv** nous allons utiliser un outil appelé **pip**.

**Installation de pip:**
Téléchargez <a href="https://bootstrap.pypa.io/get-pip.py">ce fichier</a> puis lancez dans un shell:

    $ python get-pip.py

**Installation de virtualenv:**
Maintenant que nous avons **pip**, nous pouvons installer **virtualenv** facilement: 

    $ pip install virtualenv

Maintenant, il faut créer l'environnement isolé pour le projet:

    $ virtualenv chemin/vers/me

Enfin, il faut activer cet environnement:

    $ source chemin/vers/me/bin/activate
  
 Vous êtes maintenant dans un environnement isolé pour le projet, vous pouvez installer des modules qui seront propres à cet environnement !

Pour sortir de cet environnement:

    $ desactivate

**Installation de python-nmap (ou d'un quelconque autre module):**

    $ pip install python-nmap

Objectifs pour la release 1.0
-------------
- Faire un système pour référencer tous les fichiers
- Créer un système de recherche parmi ces fichiers
- Créer une interface

Objectifs plus à long terme
-------------
- ?


Outils utilisés pour le projet
-------------

Cette rubrique référencera principalement les bibliothèques utilisées pour ce projet.

**Problème**    | **Outil**
-------- | ---
Interaction avec les serveurs FTP  | ftplib
Utilisation de nmap | **python-nmap**
Recherche parmi les fichiers   | ???
Extraire les informations pertinentes des noms de fichier | ??? 


Les outils en gras sont des modules à télécharger.
