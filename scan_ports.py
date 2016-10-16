#!/usr/bin/env python

import os
import nmap
import sys
from ftplib import FTP
import socket

class FTPScanner:

    """
    Cette classe est chargee de trouver les serveurs FTP sur une plage d'adresses
    """

    def __init__(self, range="127.0.0.1"):

        """
        Constructeur, prend en argument optionnel la plage d'adresse a scanner
        """

        self.setAddressRange( range )	

        # Creation de l'instance de nmap
        try:
            self.nmap = nmap.PortScanner()
        except nmap.PortScannerError:
            raise Exception('Nmap not found', sys.exc_info())

        except:
            raise Exception("FTPScanner init: Unexpected error:", sys.exc_info()[0])

    def setAddressRange( self, range ):
        self.addressRange = range

    def getAddressRange( self ):
        return self.addressRange

    def scan( self ):

        """
        Fonction pour executer le scan, retourne une liste de hosts ayant le port 21 ouvert.
        """

        """
        Execute un scan nmap avec comme option:
        -Pn : Ne cherche pas a savoir si l'host est en ligne
        -T4 : Accelere le scan
        -p21: On scanne le port 21
        -n  : Ne fait pas de DNS discovery (accelere le scan)
        """
        self.nmap.scan(hosts=self.addressRange, arguments='-Pn -T4 -p21 -n')
        hostsScanned = self.nmap.all_hosts()
        hostsWithFTP = []
        for host in hostsScanned:
            if self.nmap[host]["tcp"][21]["state"] == "open":
                # On essaie de s'y connecter avec FTP pour verifier que c'est bien un serveur FTP
                try:
                    ftp = FTP(host, timeout=1)
                    ftp.login()
                except:
                    print("FTPScan: Could not connect to FTP server " + host, sys.exc_info())
                else:
                    ftp.close()
                    hostsWithFTP += [host]

        return hostsWithFTP

s = FTPScanner("157.159.41-49.0/24")
print("Machines avec un serveur FTP sur la plage: "+s.getAddressRange())
for addr in s.scan():
    print(" - " + addr)