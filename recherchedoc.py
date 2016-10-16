#!/usr/bin/env python
from ftplib import FTP
import os
class Recherche:

    
    def __init__(self, range, charset):
        """Constructeur de notre classe"""
        self.range = range
        self.usrsearch = charset

    def affichedoc(self):
    	ftp = FTP(self.range)
        ftp.login()
        listmaindir=[]
        for i in ftp.nlst():
        	listmaindir.append(ftp.nlst(i))
        ftp.close()
        return(listmaindir)


michel = Recherche("157.159.42.42","Belliard")
print(michel.affichedoc())