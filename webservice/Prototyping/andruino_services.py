'''
    TEST CODE
'''


import os, sys
import serial
import threading
from Queue import Queue
import time
import math
from struct import *
from datamaps import *



class AndrSerial(threading.Thread):
    
    def __init__(self, SerialInterfaceQueue, deviceType='arduino'):
        ''' 
            Setup serial interface
            
            readSleepInterval - This is the amount of time the thread will wait before 
                            sending a read instruction to the AVR and return the result.
                            Each read operation will pull the state of the device from the AVR
                            and store the response in the database. 
                            In debug mode, thread will display raw output to the screen.
            QueuePollInterval - Amount of time tread will wait before checking for messages 
                            on the serialInterfaceQueue...    
        '''
        self.map = deviceMap(deviceType)
        
        self.ReadSleepTime = 10
        self.QueuePollInterval = 0.5
        self.serialQueue = SerialInterfaceQueue
        '''
            Initialize this thread
        '''
        self.ThreadRunState = 0
        self.ThreadRunStatus = False
        threading.Thread.__init__(self)
        self.StopMe = threading.Event()
        
        # setup the serial port
        self.ser = serial.Serial('/dev/ttyAvr', 115200, timeout=0.25)
        # Wait for the serial post to initialize
        print "Thread is sleeping before starting..."
        time.sleep(15)

        self.serialMsg = {
            'ID':None,
            'TYPE': None,
            'DATA': None
        }
        
        
    def run(self):
        '''
            Start the thread
        '''
        self.ThreadRunState = 1
        self.initAvr()
        
        '''
            Wait until the controller is ready
        '''
        
        
        while self.ThreadRunState:
            '''
                do this alot
            '''
            self.ThreadRunStatus = True
            self.readAvr()
            #self.printMap()
            
            
            '''
                Sleep for a period of time before starting up again...
            '''
            waitTime = math.ceil(self.ReadSleepTime / self.QueuePollInterval)
            waitTime = int(waitTime)
            #print "Going to scan %s times" % (str(waitTime))
            for s in range(1 , waitTime):
                msg = self.getMsg() 
                if msg != None:
                    '''
                        Do something if a message is on the queue
                    '''
                    #print "Got a message -> %s " % (msg)
                    self.parseMsg(msg)
                time.sleep(self.QueuePollInterval)
        
        '''
            Thread looping finished 
            Clean up and exit program
        '''
        self.cleanup()
        
    def getMap(self):
        '''
            Return IO map
        '''
        return self.map.getMap()
    
    def printMap(self):
        thisMap = self.map.getMap()
        print "Map: %s " % (thisMap)

    def parseMsg(self, msgData):
        '''
            Parse content of messages on queue
            verify data is correct
            read message request, determine what operation to perform
        '''
        #print "Parsing message %s" % (msgData)
        if (msgData['TYPE'] == 'READ'):
            '''
                Read request operation
            '''
            self.readAvr()
                        
        else:
            '''
                All other operations
            '''
            avrWrite = self.map.pinToMap(msgData)
            self.writeAvr(avrWrite['ADDR'], avrWrite['VALUE'])
            ''' Sleep longer than the timeout'''
            time.sleep(0.5)
            self.readAvr()
            
            
            
    
       
        
    def initAvr(self):
        '''
            Put arduino in run mode
        '''
        print "waking up avr"
        self.ser.write('#')
        data = self.readAvr()
        print "Arduino Said %s" % (data)

        
    def readAvr(self):
        '''
            Read data from arduino
        '''
        
        self.ser.write('r')
        dataSet = self.ser.readlines()
        '''
            Remove trailing line feed carriage return 
        '''
        for data in dataSet: 
            data = data.strip()
            self.map.updateMap(data)
            #self.printMap()
        
        
    
    
    def writeAvr(self, addr, data):
        '''
            Write message to AVR controller
            
        '''
        ThisReq = "w%s%s" % (addr, data)      
        HexAddr = pack('B1', int(addr))
        HexData = pack('B1', int(data))
        
        #ThisReq = "\x77%s%s" % (HexAddr, HexData)
        print "---Sending this to the AVR %s" % (ThisReq)
        try:
            self.ser.write('\x77%s%s' % (HexAddr, HexData))
        except SerialException:
            return None
        
        
    
    def getMsg(self):
        '''
            Check for requests on the command queue
            If a message is found then read the data and 
            pass the message back
        '''
        
        if self.serialQueue.empty():
            '''
                If there are no instructions found waiting on the queue
                then return None. 
            '''
            return None
        else: 
            '''
                If a message is available on the Queue remove the data 
                pass it to the calling request
            '''
            return self.serialQueue.get()
        
        
    def stop(self):
        '''
            Stop the tread and close out reasources...
        '''
        self.ThreadRunState = 0
    
    def cleanup(self):
        '''
            Clean up open connections prior to exiting
        '''
        self.ThreadRunStatus = False
        self.ser.close()
        
    def getStatus(self):
        '''
            Return Thread run status
        '''
        return self.ThreadRunStatus
        

    
    def getMsgSyntax (self):
        '''
            Return message syntax
        '''
        self.serialMsg['ID'] = "<Message ID>"
        self.serialMsg['TYPE'] = "<Type of request read or write>"
        self.serialMsg['DATA'] = "<Message payload>" 
        
        return self.serialMsg

"""

class AndrEmail(threading.Thread):
    '''
        Email generator thread
    '''
    def __init__(self, SmtpServer=None, EmailAcct=None, EmailPw=None):
        threading.Thread.__init__()
        self.MyEmailAddr = EmailAcct


    def senfMsg(self, Subject='No Subject Set', Addr, msg='Default Message' ):

        format = '''\
To: %s
From: %s
Subject: %s
%s
''' % (Addr, self.MyEmailAddr, Subject, msg)
        
"""

if __name__ == '__main__':
    '''
        Run some tests
    '''
    try:
        bar = Queue(0)
        foo = AndrSerial(bar)
        foo.start()
        ''' 
            Wait 5 minutes, then publish a message to the queue
        '''
        time.sleep(45)
        bar.put('Hello')
        time.sleep(30)
        '''
            Run application 
        '''
        #foo.stop()
    except KeyboardInterrupt:
        sys.exit(0)
    
    
'''
cmd line examples

format = """\
To: %s
From: %s
Subject: %s
%s
""" % (

'''
        



    
