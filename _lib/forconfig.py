#!/usr/bin/python3
#Copyright Xoristzatziki 

import configparser 
import os,sys

class MyConfigs():
    def __init__(self,filename):
        self.myconfigfilename = filename
        
    def readconfigvalue(self, wichsection, wichoption, default):
        try:
            cp = configparser.ConfigParser()
            cp.read(self.myconfigfilename)
            return cp.get(wichsection,wichoption)
        except configparser.NoSectionError:
            return default
        except:#oops...
            print("Exception: ", str(sys.exc_info()) )
            return default
            
    def writeconfigvalue(self, whichsection, whichoption, whichvalue): 
        b = os.path.split(self.myconfigfilename)
        b = os.path.join(b[:-1])
        if not os.path.isdir(b[0]):
            os.makedirs(b[0])#self.myconfigfilename)
        cp = configparser.ConfigParser()
        cp.read(self.myconfigfilename)
        #print dir(cp)
        if cp.has_section(whichsection):
            pass
        else:
            cp.add_section(whichsection)
        cp.set(whichsection, whichoption, whichvalue)
        #cp.set('main','width',whichvalue)
        with open(self.myconfigfilename, 'w') as f:
            cp.write(f)
            #print self.myconfigfilename

if __name__ == "__main__":
    #print pygtk
    # get the real location of this launcher file (not the link location)
    #realfile = os.path.realpath(__file__)
    inifile = os.path.join(os.path.expanduser('~'),'OCPany.conf')
    test = MyConfigs(inifile)
    test.writeconfigvalue('somesection',someparameter','avalue')

