<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- The above 3 meta tags *must* come first in the head; any other head content must come *after* these tags -->
    <meta name="description" content="">
    <meta name="author" content="">

    <title>MAISEL Explorer</title>

    <!-- Latest compiled and minified CSS -->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">

    <!-- Optional theme -->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap-theme.min.css" integrity="sha384-rHyoN1iRsVXV4nD0JutlnGaslCJuC7uwjduW9SVrLvRYooPp2bWYgmgJQIXwl/Sp" crossorigin="anonymous">

    <!-- Latest compiled and minified JavaScript -->
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js" integrity="sha384-Tc5IQib027qvyjSMfHjOMaLkfuWVxZxUPnCJA7l2mCWNIpG9mGCD8wGNIcPD7Txa" crossorigin="anonymous"></script>

    <!-- Custom styles for this template -->
    <link href="dashboard.css" rel="stylesheet">


    <script> var ftp_servers = [{{!ftpserv}}]; </script>
    <script src="https://cdn.socket.io/socket.io-1.4.5.js"></script>
  </head>

  <body>
    <nav class="navbar navbar-inverse navbar-fixed-top">
      <div class="container-fluid">
        <div class="navbar-header">
          <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar" aria-expanded="false" aria-controls="navbar">
            <span class="sr-only">Toggle navigation</span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </button>
          <a class="navbar-brand" href="#">MAISEL Explorer 6.0</a>
        </div>
        <div id="navbar" class="navbar-collapse collapse">
          <ul class="nav navbar-nav navbar-right">
            <li><a href="#">Recherche avancée</a></li>
            <li><a href="#">Serveurs</a></li>
            <li><a href="#">Contact</a></li>
          </ul>
          <form class="navbar-form navbar-right" id="me_recherche" >
            <input type="text" id="me_recherche_champ" class="form-control" placeholder="Recherche...">
          </form>
        </div>
      </div>
    </nav>

    <div class="container-fluid">
      <div class="row">
        <div class="col-sm-3 col-md-2 sidebar">
          <ul class="nav nav-sidebar">
            <li class="active"><a href="#">Tout<span class="sr-only">(current)</span></a></li>
            <li><a href="#">Films</a></li>
            <li><a href="#">Séries</a></li>
            <li><a href="#">Animes</a></li>
            <li><a href="#">Jeux</a></li>
            <li><a href="#">Autres</a></li>
          </ul>
          <ul class="nav nav-sidebar">
            <li><a href="">Serveur 1</a></li>
            <li><a href="">Serveur 2</a></li>
            <li><a href="">Serveur 3</a></li>
          </ul>
        </div>
        <div class="col-sm-9 col-sm-offset-3 col-md-10 col-md-offset-2 main">
         <h1 class="page-header">Arborescence</h1>
          <div class="table-responsive">
            <table class="table table-striped">
              <thead>
                <tr>
                  <th class="col-md-6">Nom</th>
                  <th class="col-md-1">Date MàJ</th>
                  <th class="col-md-2">Serveur</th>
                  <th class="col-md-1">Catégorie</th>
                  <th class="col-md-1">Taille</th>
                  <th class="col-md-1">Télécharger</th>
                </tr>
              </thead>
              <tbody id="me_fichiers">
                <!--
                <tr>
                    <td>Trueman show</td>
                    <td>10/10/2010</td>
                    <td>157.159.256.256</td>
                    <td>Film</td>
                    <td>3 GiB</td>
                    <td><button type="button" class="btn btn-primary">Télécharger</button></td>
                </tr>
                <tr>
                    <td>Shutter island</td>
                    <td>01/12/2012</td>
                    <td>157.159.256.257</td>
                    <td>Film</td>
                    <td>521 MiB</td>
                    <td><button type="button" class="btn btn-primary">Télécharger</button></td>
                </tr>

                <tr>
                    <td>One piece épisode 5e10</td>
                    <td>10/03/1945</td>
                    <td>157.159.256.256</td>
                    <td>Anime</td>
                    <td>200 MiB</td>
                    <td><button type="button" class="btn btn-primary">Télécharger</button></td>
                </tr>

                <tr>
                    <td>Garry's mod</td>
                    <td>10/08/2050</td>
                    <td>157.159.256.256</td>
                    <td>Jeux</td>
                    <td>30 GiB</td>
                    <td><button type="button" class="btn btn-primary">Télécharger</button></td>
                </tr>
                -->


              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>

    <!-- Bootstrap core JavaScript
    ================================================== -->
    <!-- Placed at the end of the document so the pages load faster -->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
    <script>window.jQuery || document.write('<script src="../../assets/js/vendor/jquery.min.js"><\/script>')</script>
    <script src="../../dist/js/bootstrap.min.js"></script>
    <!-- Just to make our placeholder images work. Don't actually copy the next line! -->
    <script src="../../assets/js/vendor/holder.min.js"></script>
    <!-- IE10 viewport hack for Surface/desktop Windows 8 bug -->
    <script src="../../assets/js/ie10-viewport-bug-workaround.js"></script>
    <script src="js/maiselexplorer.js"></script>
  </body>
</html>
