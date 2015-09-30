'''
    API Provides the following:
    1.) Define API for interacting with shared database resource...
    2.) Interface for andruino services

Arduino Pin Map

0 = Port


'''

import datetime
from Queue import Queue
from andruino_services import *
import time, sys
from andruino_db import AndruinoDb

class AndruinoApi():
    def __init__(self, DeviceId=None ):
        '''
            Queue interfaces for messaging
        '''
        self.dbi = AndruinoDb()
        if not DeviceId:
            print "[API] DeviceId required. Please set device ID "
            sys.exit()
        else:
            '''
                Set Device ID for this implementation of the API
            '''
            self.device_id=DeviceId
        
        
        '''
            Create messaging queues for interacting with the threads.
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
        
              
    def startSerial(self, ):
        '''
            Start the serial thread for this device
            thread will be bound to the serial interface defined within the devices table
            All calls to the thread interfaces will be bound to a unique device 
        '''
        self.serialThread = AndrSerial(self.serialQueue, self.device_id)
        self.serialThread.start()
        
        '''
            Place Messages in queue to set device configuration base
            on config data from the database.
            Note: Threads are bound to a particular device_id. So id 
            does not need to be set. 
        '''
        self.writeConfig()

        
        # TODO 
        '''
            Add interface for starting email thread...
        '''
        
        
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

    def writeOutput(self, DetailId, Value):
        '''
            Requires DetailId...
            Read state from the database 
        '''
        ConfigSettings = self.dbi.getConfig(DetailId)
        intValue = int(Value)
        for Setting in ConfigSettings:
            self.setOutput(Setting['pin'], intValue)

    def writeConfig(self, DetailId=None):
        '''
            Write the pin config data to the database.
            
            One Parameter
            DetailId - Represents the Pin stored as id in the details table.
            When DetailId is set only that device will be written to the serial interface
            
            if the parameter DetailId is not passed in, value defaults to None.
            In this condition, all devices within self.DeviceId will be initialized. 
            
        '''
        ConfigSettings = self.dbi.getConfig(DetailId)
        for Setting in ConfigSettings:
            '''
                Process all rows returned from database
                run config on each row. 
                
                If DetailId is set only one row will be returned
            '''
            print "Settings Pin %s - Config %s" % (Setting['pin'], Setting['config'])
            self.setConfig(Setting['pin'], Setting['config'])
        
        
        
        

    def getAvrMap(self):
        '''
            Get the IO map from the thread
            returns dictionary of ports and OI states
        '''
        return self.serialThread.getMap()




if __name__ == '__main__':

    '''
        Updated with database models
    '''
    #api = AndruinoApi(DeviceId=1)
    #api.startSerial()
    
    
    #time.sleep(25)
    #api.writeConfig()
    
    """
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
    """