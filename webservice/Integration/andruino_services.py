'''
    TEST CODE
'''

import smtplib
import os, sys
import serial
import threading
from Queue import Queue
import time
import math
from struct import *
from datamaps import *
from andruino_db import AndruinoDb



class AndrSerial(threading.Thread):
    
    def __init__(self, SerialInterfaceQueue, device_id, deviceType='arduino'):
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
        ready_sleep_timeout = 20
        self.map = deviceMap(deviceType)
        self.pinMap = self.map.getPinMap()
        self.dbi = AndruinoDb()
        self.ReadSleepTime = 10
        
        self.QueuePollInterval = 0.5
        self.serialQueue = SerialInterfaceQueue
        self.device_id = device_id
        self.emailSettings = {}
        '''
            Initialize this thread
        '''
        
        
        self.ThreadRunState = 0
        self.ThreadRunStatus = False
        threading.Thread.__init__(self)
        self.StopMe = threading.Event()
        
        device_port = self.dbi.getDeviceById(self.device_id)
        
        # setup the serial port
        try:
            self.ser = serial.Serial(device_port['port'], 115200, timeout=0.25)
        except serial.SerialException:
            '''
                If port can not be opened...
            '''
            print """Failed to open port [%s]\nCheck your configuration and try again""" % device_port['port']
            sys.exit(2)
            
        # Wait for the serial post to initialize
        print "Thread is sleeping before starting..."
        time.sleep(ready_sleep_timeout)

        self.serialMsg = {
            'ID':None,
            'TYPE': None,
            'DATA': None
        }
        
        
    def run(self):
        '''
            Start the Serial thread
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
            '''
                Read data from the AVR
            '''
            try:
                self.readAvr()
            except serial.SerialException, why:
                print "Failed to read from device: %s" %(why)
                sys.exit(2)
            
            '''
                UnComment to print debug map
            '''
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
                    print "Got a message -> %s " % (msg)
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
        try:
            '''
                Attempt to read data from the serial port
            '''
            self.ser.write('r')

        except serial.SerialException:
            print "General Serial port Failure attempting to write."
            sys.exit(2)
        except serial.SerialTimeoutException:
            print "Serial Port Timed out attempting to read device"
            sys.exit(3)
        except OSError:
            print "Error managing serial port. Its dead Jim."
            sys.exit(3)
            
        dataSet = self.ser.readlines()
        '''
            Remove trailing line feed carriage return 
        '''
        for data in dataSet: 
            '''
                Get Raw data
            '''
            data = data.strip()
            '''
                Update the data map
            '''
            self.map.updateMap(data)

        '''
            Update the db
        '''
        self.updateDb()
        
    def convertInt(self, intVal):
        '''
            Convert integer to binary array
            Example
            >>> intVal = 25
            >>> bitCount=8
            >>> [str((intVal >> BitPosition) & 1) for BitPosition in range(bitCount-1, -1, -1)]
            ['0', '0', '0', '1', '1', '0', '0', '1']
        '''
        ''' Set bit count. Could be used for other conversions '''
    
        
        bitCount = 8
        return [(intVal >> BitPosition) & 1 for BitPosition in range(bitCount-1, -1, -1)]
    
    
    
    def updateDb(self):
        '''
            Get the map and process changes.
            This is the synchronous activity used 
            to update the database with changes pulled 
            from the device...
        '''
        RegMap = self.map.getMap()
        #print "Processing Map -> %s" % RegMap
        for RegGrp in RegMap:
            '''
                Get the map from the avr
                process changes in the database
                Map: {'C': {'DDR': 0, 'PORT': 0, 'PIN': 0}, 'B': {'DDR': 32, 'PORT': 0, 'PIN': 0}, 'D': {'DDR': 0, 'PORT': 1, 'PIN': 3}} 
            '''
            
            #print "Updating Register -> %s" % RegGrp
            '''
                Only update the PORT and PIN Registers 
                Since the DDR register is managed by config
            '''
            if RegGrp != 'C':
                '''
                    This version will not support the analog channel (Register C)
                '''
                
            
                '''
                    Convert for pin mapping
                '''
                pinMap = self.pinMap[RegGrp].split(':')
                binPosition = 0
                
                
                '''
                Convert register decimal value to binary arrays
                Reverse order for proper indexing
                '''
                
                
                #print "INTEGER - DDR:%s , PORT:%s, PIN:%s" % (RegMap[RegGrp]['DDR'], RegMap[RegGrp]['PORT'], RegMap[RegGrp]['PIN'])
                ddrBits = self.convertInt(RegMap[RegGrp]['DDR'])
                portBits = self.convertInt(RegMap[RegGrp]['PORT']) 
                pinBits =  self.convertInt(RegMap[RegGrp]['PIN'])
                #print "DDR:%s , PORT:%s, PIN:%s" % (ddrBits, portBits, pinBits)
                ddrBits.reverse()
                portBits.reverse()
                pinBits.reverse()
                #print "REVERSED - DDR:%s , PORT:%s, PIN:%s" % (ddrBits, portBits, pinBits)

                
                #print "-Processing Register %s" % RegGrp
    
                for pin in range(int(pinMap[0]), int(pinMap[1])+1):
                    '''
                        Record the value of each pin per register 
                        
                        self.device_id
                    '''
                    
                    if ddrBits[binPosition] == 1:
                        '''
                            Read Port register only update pins that are outputs
                        '''
                        #print "[OUTPUT] UPDATE details SET hw_value = %s, hw_ts=datetime('now', 'localtime') WHERE pin = %s AND device_id  = %s" % (portBits[binPosition], pin, self.device_id)
                        sql = "UPDATE details SET hw_value = %s, hw_ts=datetime('now', 'localtime') WHERE pin = %s AND device_id  = %s" % (portBits[binPosition], pin, self.device_id)
                        
                        #print "Pin [%s] is an output" % pin
                    else:
                        '''
                            Read PIN register only update pins that are inputs. 
                        '''
                        #print "[INPUT] UPDATE details SET hw_value = %s, hw_ts=datetime('now', 'localtime') WHERE pin = %s AND device_id  = %s" % (pinBits[binPosition], pin, self.device_id)
                        #print "Pin [%s] is an INPUT" % pin
                        
                        sql = "UPDATE details SET hw_value = %s, hw_ts=datetime('now', 'localtime') WHERE pin = %s AND device_id  = %s" % (pinBits[binPosition], pin, self.device_id)
                    #print sql
                    
                    
                    self.dbi.exec_sql(sql)
                    binPosition += 1
                

            
        
        
    
    
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

    

    
    def sendAlert(self, Subject='No Subject Set', msg='Default Message'  ):
        '''
            Send email 
        '''
        thismsg = msg
        server = smtplib.SMTP('smtp.gmail.com',587)
        server.ehlo()
        server.starttls()
        server.login('addr','mypass')
        server.sendmail('myname@gmail.com','somename@somewhere.com',thismsg)
        server.close()
         
        
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
        

"""
DDR:[1, 0, 0, 1, 1, 0, 0, 0] , PORT:[0, 0, 0, 0, 0, 0, 0, 0], PIN:[0, 0, 0, 0, 0, 0, 0, 0]
[OUTPUT] UPDATE details SET hw_value = 0, hw_ts=datetime('now', 'localtime') WHERE pin = 8 AND device_id  = 1
[INPUT] UPDATE details SET hw_value = 0, hw_ts=datetime('now', 'localtime') WHERE pin = 9 AND device_id  = 1
[INPUT] UPDATE details SET hw_value = 0, hw_ts=datetime('now', 'localtime') WHERE pin = 10 AND device_id  = 1
[OUTPUT] UPDATE details SET hw_value = 0, hw_ts=datetime('now', 'localtime') WHERE pin = 11 AND device_id  = 1
[OUTPUT] UPDATE details SET hw_value = 0, hw_ts=datetime('now', 'localtime') WHERE pin = 12 AND device_id  = 1
[INPUT] UPDATE details SET hw_value = 0, hw_ts=datetime('now', 'localtime') WHERE pin = 13 AND device_id  = 1
DDR:[0, 0, 0, 0, 0, 1, 1, 1] , PORT:[1, 0, 0, 0, 0, 0, 0, 0], PIN:[1, 1, 0, 0, 0, 0, 0, 0]
[INPUT] UPDATE details SET hw_value = 1, hw_ts=datetime('now', 'localtime') WHERE pin = 0 AND device_id  = 1
[INPUT] UPDATE details SET hw_value = 1, hw_ts=datetime('now', 'localtime') WHERE pin = 1 AND device_id  = 1
[INPUT] UPDATE details SET hw_value = 0, hw_ts=datetime('now', 'localtime') WHERE pin = 2 AND device_id  = 1
[INPUT] UPDATE details SET hw_value = 0, hw_ts=datetime('now', 'localtime') WHERE pin = 3 AND device_id  = 1
[INPUT] UPDATE details SET hw_value = 0, hw_ts=datetime('now', 'localtime') WHERE pin = 4 AND device_id  = 1
[OUTPUT] UPDATE details SET hw_value = 0, hw_ts=datetime('now', 'localtime') WHERE pin = 5 AND device_id  = 1
[OUTPUT] UPDATE details SET hw_value = 0, hw_ts=datetime('now', 'localtime') WHERE pin = 6 AND device_id  = 1
[OUTPUT] UPDATE details SET hw_value = 0, hw_ts=datetime('now', 'localtime') WHERE pin = 7 AND device_id  = 1


DDR:[0, 0, 0, 1, 1, 0, 0, 1] , PORT:[0, 0, 0, 0, 0, 0, 0, 0], PIN:[0, 0, 0, 0, 0, 0, 0, 0]
REVERSED - DDR:[1, 0, 0, 1, 1, 0, 0, 0] , PORT:[0, 0, 0, 0, 0, 0, 0, 0], PIN:[0, 0, 0, 0, 0, 0, 0, 0]
[OUTPUT] UPDATE details SET hw_value = 0, hw_ts=datetime('now', 'localtime') WHERE pin = 8 AND device_id  = 1
[INPUT] UPDATE details SET hw_value = 0, hw_ts=datetime('now', 'localtime') WHERE pin = 9 AND device_id  = 1
[INPUT] UPDATE details SET hw_value = 0, hw_ts=datetime('now', 'localtime') WHERE pin = 10 AND device_id  = 1
[OUTPUT] UPDATE details SET hw_value = 0, hw_ts=datetime('now', 'localtime') WHERE pin = 11 AND device_id  = 1
[OUTPUT] UPDATE details SET hw_value = 0, hw_ts=datetime('now', 'localtime') WHERE pin = 12 AND device_id  = 1
[INPUT] UPDATE details SET hw_value = 0, hw_ts=datetime('now', 'localtime') WHERE pin = 13 AND device_id  = 1
DDR:[1, 1, 1, 0, 0, 0, 0, 0] , PORT:[0, 0, 0, 0, 0, 0, 0, 1], PIN:[0, 0, 0, 0, 0, 0, 1, 1]
REVERSED - DDR:[0, 0, 0, 0, 0, 1, 1, 1] , PORT:[1, 0, 0, 0, 0, 0, 0, 0], PIN:[1, 1, 0, 0, 0, 0, 0, 0]
[INPUT] UPDATE details SET hw_value = 1, hw_ts=datetime('now', 'localtime') WHERE pin = 0 AND device_id  = 1
[INPUT] UPDATE details SET hw_value = 1, hw_ts=datetime('now', 'localtime') WHERE pin = 1 AND device_id  = 1
[INPUT] UPDATE details SET hw_value = 0, hw_ts=datetime('now', 'localtime') WHERE pin = 2 AND device_id  = 1
[INPUT] UPDATE details SET hw_value = 0, hw_ts=datetime('now', 'localtime') WHERE pin = 3 AND device_id  = 1
[INPUT] UPDATE details SET hw_value = 0, hw_ts=datetime('now', 'localtime') WHERE pin = 4 AND device_id  = 1
[OUTPUT] UPDATE details SET hw_value = 0, hw_ts=datetime('now', 'localtime') WHERE pin = 5 AND device_id  = 1
[OUTPUT] UPDATE details SET hw_value = 0, hw_ts=datetime('now', 'localtime') WHERE pin = 6 AND device_id  = 1
[OUTPUT] UPDATE details SET hw_value = 0, hw_ts=datetime('now', 'localtime') WHERE pin = 7 AND device_id  = 1



sqlite> select * from details where config = 1;
3|1|default_5|1|5|0|0|2011-04-17 19:16:28|2011-04-19 18:16:39|1
4|1|default_6|1|6|1|0|2011-04-17 20:23:27|2011-04-19 18:16:39|1
5|1|default_7|1|7|0|0|2011-04-17 20:23:41|2011-04-19 18:16:39|1
8|1|default_10|1|10|0|0|2011-04-17 20:24:47|2011-04-19 18:16:49|1
9|1|default_11|1|11|0|0|2011-04-19 22:12:03|2011-04-19 18:16:39|1



"""    

    
