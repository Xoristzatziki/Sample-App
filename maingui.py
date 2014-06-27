#!/usr/bin/python3
#Copyright Xoristzatziki

################## IMPORTS ################## 
import os, sys
import glob
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GdkPixbuf

import time
import datetime
from time import gmtime, strftime
from datetime import date

import threading
import subprocess
import re

from collections import deque

import _lib.forconfig as myconfig

from _lib.MyDialogs import *
#or:
#from _lib.MyDialogs import YesCancelDialog as YesCancelDialog
#from _lib.MyDialogs import InputBox as InputBox
#from _lib.MyDialogs import FileChoose as FileChoose

################## Constants ################## 
APPNAME = 'Base App'
version = '0.0.1'
comments = 'A basic gui for an application with python3 and Glade using Gtk3+'

#Some color samples that will be used my Window
COLOR_OK = '#228b22'
COLOR_WORK = '#D92F2F'

################## Classes ################## 
class UserSettings:
    '''Keeps tracking of user's gui preferences
    
    '''
    def __init__( self):
        self.windowMain = { 'W' : 640,
                'H' : 480,
                'Maximized' : False}


class MainGui:    
    def __init__(self, realfile_dir):
        #Initializing the gtk's thread engine
        #Gtk.threads_init()

        #in case we want to use more than one but named instance
        self.InstanceName = 'OCP' + APPNAME + '-' + version + '-' + str(time.time())
        #print self.InstanceName
        self.start_time = 0.
        self.MyAppPath = realfile_dir        
        self.MySettingsFile = myconfig.MyConfigs(os.path.expanduser(os.path.join('~', '.OCP-' + APPNAME , 'OCP.conf')))
        self.MyBuilder = Gtk.Builder()
        self.US = UserSettings()
        self.MyBuilder.add_from_file(os.path.join(self.MyAppPath, '_glades', "maingui.glade"))
        self.MyBuilder.connect_signals(self)
        self.MyMainWindow = self.MyBuilder.get_object("windowMain")
        self.icon = GdkPixbuf.Pixbuf.new_from_file(os.path.join(os.getcwd(), '_icons', "logo.png"))
        self.logo = GdkPixbuf.Pixbuf.new_from_file(os.path.join(os.getcwd(), '_icons', "logo64.png"))
        self.MyMainWindow.set_icon(self.icon)
        self.MyMainWindow.set_title(APPNAME + u' ' + version)
        self.MyBuilder.get_object('lblVersion').set_label('Version: ' + version + ' ')
        #read config values
        #print self.ohoho.get_object("vpaned1").get_position() , '#2'
        #By default stock icons on buttons are disabled
        #gtksettings = Gtk.Settings.get_default()
        #gtksettings.props.gtk_button_images = True

        self.MyMainWindow.modify_bg(Gtk.StateType.NORMAL, Gdk.color_parse("#228b22"))#forest green
        #I want my window almost maximized for the first time
        #screenW = self.MyMainWindow.get_screen().get_width()
        #screenH = self.MyMainWindow.get_screen().get_height() - 150
        #But you maybe not...
        screenW = 150
        screenH = 200
             
        self.US.windowMain['W'] = int(self.MySettingsFile.readconfigvalue('windowMain','W',str(screenW)))
        self.US.windowMain['H'] = int(self.MySettingsFile.readconfigvalue('windowMain','H', str(screenH)))
        self.MyMainWindow.resize(self.US.windowMain['W'],self.US.windowMain['H'])
        if self.MySettingsFile.readconfigvalue('windowMain','maximized','True')  == 'True':
              self.MyMainWindow.maximize()
        self.MyMainWindow.show()
        #set focus to something here
        #self.mymainwindow.set_focus(self.txtsearchtext)#set focus to entry text

        Gtk.main()
        
    ####################################################### General "self" functions ####################################
    def savemysetings(self):
        '''Saves user preferences.
        
        '''
        #print 'saving...'
        #print('windowMain','height',str(self.US.H))
        self.MySettingsFile.writeconfigvalue('windowMain','W',str(self.US.windowMain['W']))
        self.MySettingsFile.writeconfigvalue('windowMain','H',str(self.US.windowMain['H']))
        self.MySettingsFile.writeconfigvalue('windowMain','maximized',str(self.US.windowMain['Maximized']))

    def showabout(self):
        '''Shows the about dialog.
        
        '''
        #maybe a smaller version of icon?
        dialog = AboutBox(APPNAME,version,self.MyMainWindow,self.logo,self.MyAppPath,comments)
        response = dialog.run()
        dialog.destroy()       

    def runthecommand(self):
        '''
        
        '''
        thecommandentry = self.MyBuilder.get_object("txtcommand")
        #WARNING! running the command with shell=True is a security hazard
        #We also use here stderr=subprocess.STDOUT in order to get the errors as well
        output = subprocess.check_output(thecommandentry.get_text(),stderr=subprocess.STDOUT,shell=True)
        #just for debug purposes
        print(output)
        theoutputlabel = self.MyBuilder.get_object("lblOutput")
        theoutputlabel.set_text(output.decode('utf-8'))
        

    ####################################################### Widget and window events (on_..._clicked etc) ####################################
    def on_windowMain_destroy(self, *args):
        '''Does all clearings upon exit.
            
            Also calls a function to save user preferences.
        '''
        self.savemysetings()        
        Gtk.main_quit(*args)

    def on_bexit_clicked(self, *args):
        '''Calls main exit function.
        
        '''
        self.on_windowMain_destroy()

    def on_brun_clicked(self, *args):
        '''Runs the command.
        
        '''
        self.runthecommand()

    def on_babout_clicked(self, *args):
        '''Calls the about function.
        
            Displays the about box.
        '''
        self.showabout()
        #or... display the about box writing code here
        #and not calling another function.

################## Function that runs the program if the python file is called directly ################## 
#(Either as an executable or by:
#python3 thenameofthepythonfile
#aka python3 maingui.py)
if __name__ == "__main__":
    #print pygtk
    # get the real location of this launcher file (not the link location)
    realfile = os.path.realpath(__file__)
    realfile_dir = os.path.dirname(os.path.abspath(realfile))
    test = MainGui(realfile_dir)
