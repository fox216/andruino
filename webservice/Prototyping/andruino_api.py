'''
    API Provides the following:
    1.) Define API for interacting with shared database resource...
    2.) Interface for andruino services

Arduino Pin Map

0 = Port


'''
import sqlite3
import datetime
from Queue import Queue
from andruino_services import *
import time



sql = sqlite3.connect('Arduino.db')



class AndruinoApi():
    def __init__(self):
        '''
            Queue interfaces for messaging
        '''
        self.serialQueue = Queue(0)
        self.emailQueue = Queue(0)
        '''
            Stub for accessing thread
        '''
        self.serialThread = None
        self.emailThread = None
        '''
            Map Pins to Port Interfaces
            Map must be maintained at this level for multiple device support.
        '''       
    def startSerial(self):
        self.serialThread = AndrSerial(self.serialQueue)
        self.serialThread.start()
        
    def stopSerial(self):
        self.serialThread.stop()
        
        
    def setOutput(self, pinNumber, pinState):
        '''
            This method is used to set 
            Set ouput state of a pin attached to the avr controller
            Pin Numbers = 2-13 (0 & 1 reserved for serial communication)
            Pin State = 0 or 1 
            THIS SECTION SUPPORTS PORT INTERFACE ONLY (Change IO) 
            TODO: Add multiple devices (Phase 2)
        '''
        
        
        #self.serialThread.setOutput(pinNumber,pinState)
        '''
            Cross reference from Ports to Hex commands
        '''
        
        msg = {
               'ID': int(time.time()),
               'TYPE': 'WRITE',
               'DATA': "%s:%s" % (pinNumber, pinState),
               'STATE': pinState
        }
        self.serialQueue.put(msg)

    def setConfig(self, pinNumber, pinMode):
        '''
            This method is used to set 
            Set ouput state of a pin attached to the avr controller
            Pin Numbers = 2-13 (0 & 1 reserved for serial communication)
            Pin State = 0 or 1 
            THIS SECTION SUPPORTS PORT INTERFACE ONLY (Change IO) 
            TODO: Add multiple devices (Phase 2)
        '''
        
        
        #self.serialThread.setOutput(pinNumber,pinState)
        '''
            Cross reference from Ports to Hex commands
        '''
        
        msg = {
               'ID': int(time.time()),
               'TYPE': 'CFG',
               'DATA': "%s:%s" % (pinNumber, pinMode)
        }
        self.serialQueue.put(msg)

   

    def getAvrMap(self):
        '''
            Get the IO map from the thread
            returns dictionary of ports and OI states
        '''
        return serialThread.getMap()


if __name__ == '__main__':
    '''
        seed the database
    '''
    foo = AndruinoApi()
    foo.startSerial()
    #print "API sleeping 10 seconds"
    #time.sleep(10)
    
    print "Configure 10,and 11 as Outputs"
    foo.setConfig(11, 1)
    print "\n\n"
    foo.setConfig(10, 1)
    foo.setConfig(7, 1)
    foo.setConfig(6, 1)

    print "Configuration COMPLETE"
    
    for x in range(1,3):
        print "wait # %s" % (x)
        time.sleep(1.25)
        
    print "Set Pin 10 As Ouptut"
    foo.setOutput(10, 1)
    foo.setOutput(6, 1)
    for x in range(1,3):
        print "wait # %s" % (x)
        time.sleep(1.25)
    
    
    print "Set Pin 11 As Ouptut"
    foo.setOutput(11, 1)
    print "-------------DONE SETTING OUTPUT "

    for x in range(1,3):
        print "wait # %s" % (x)
        time.sleep(1.25)
    foo.setOutput(7, 1)
    foo.setOutput(10, 0)
      
    
    #foo.stopSerial()
