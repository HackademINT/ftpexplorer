#!/usr/bin/env python
from ftplib import FTP
class Recherche:

    
    def __init__(self, range, charset):
        """Constructeur de notre classe"""
        self.range = range
        self.usrsearch = charset
    def affichedoc(self):
    	ftp = FTP(self.range)
        ftp.login()
        print ftp.dir()
        ftp.close()
        return()


michel = Recherche("157.159.42.42","Belliard")
michel.affichedoc()