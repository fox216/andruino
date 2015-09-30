import cherrypy
import sys, os
import datetime
from struct import *
from andruino_api import *



# get the reference to the thread manager
ws_api = AndruinoApi()

'''
class SerialMgr:
    # Serial manager
    def open(self):
        # Open serial port connection
    
    def close(self):
        # Close serial port connection
     

class DeviceMgr:
    # class that stores the mapping of each device type
    
'''
class Root:
    # Root node
    @cherrypy.expose
    def index(self):
        return "Welcome to the Andruino application"

class Read:
    # Read from arduinp
    @cherrypy.expose
    def index(self):
	result = ws_api.getMap()
        return "AVR Status -> %s " % (result)
        
class Config:
    @cherrypy.expose
    def index(self,addr,state):
	ws_api.setConfig(addr, state )
        return "Configured Pin %s to Output state of %s " % (addr, state)
    
class Write:
    @cherrypy.expose
    def index(self,addr,state):
	ws_api.setOutput(addr, state)
        return "Set Pin %s to Output state of %s " % (addr, state)
        


class Start:
    @cherrypy.expose
    def index(self):
	'''
	Start the serial interface thread
	'''
	ws_api.startSerial()
        return "Thread start request Issued..." 
     
class Stop:
    @cherrypy.expose
    def index(self):
	'''
	Start the serial interface thread
	'''
	ws_api.stopSerial()
        return "Thread start request Issued..." 
     
        
        
    
if __name__ == '__main__':
    # Run this code
    root = Root()
    root.read = Read()
    root.start = Start()
    root.stop = Stop()
    root.config = Config()
    root.write = Write()

    cherrypy.quickstart(root)

    
'''
Note from -> http://tools.cherrypy.org/wiki/HTTPMethodFiltering

http://helpful.knobs-dials.com/index.php/CherryPy
'''
