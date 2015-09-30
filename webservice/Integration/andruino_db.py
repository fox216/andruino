import sqlite3
import hashlib
import datetime
import time, sys
import hashlib
from datetime import datetime

class AndruinoDb():
    def __init__(self):
        '''
            Connect to the database
        '''
        self.db_file = 'andruino.db'
        
        #self.db = sqlite3.connect(self.db_file)
        self.db = sqlite3.connect(self.db_file, check_same_thread = False)
        
        '''
            Set the database API to return dictionary of column names to data rows
        '''
        self.db.row_factory = sqlite3.Row
        '''
        self.sql = None
        self.columns = None
        '''
        self.pl = {'name':'Boarduino', 'port':'/dev/ttyAvr', 'type':'arduino', 'enabled':'1'} 
        
    
    def initDB(self):
        '''
            Execute SQL to inintialize DB
        '''
        sql = []
        sql.append("""
        CREATE TABLE "devices" (
        "id" integer primary key autoincrement, 
        "name" varchar(100) not null, 
        "port" varchar(100) not null, 
        "type" integer not null, 
        "ts_added" datetime default (datetime('now','localtime')), 
        "ts_updated" datetime default (datetime('now','localtime')), 
        "enabled" integer not null
        );
        """)
        sql.append( """
        CREATE TABLE "details" (
        "id" integer primary key autoincrement, 
        "device_id" integer not null references "devices" ("id"), 
        "label" varchar(100) not null, 
        "config" integer not null, 
        "pin" integer not null, 
        "ws_value" integer not null,
        "hw_value" integer not null, 
        "ws_ts" datetime default (datetime('now','localtime')),
        "hw_ts" datetime default (datetime('now','localtime')),   
        "enabled" integer not null
        );
        """)
        sql.append( """
        CREATE TABLE "sessions" (
            "session_id" char(128) UNIQUE NOT NULL,
            "atime" NOT NULL default (datetime('now','localtime')),
            "data" text
        );
        """)
        sql.append( """
        CREATE TABLE "users" (
        "id" integer primary key autoincrement,
        "username" varchar(32) not null,
        "password" varchar(32) not null,
        "email" varchar(64) not null
        );
        """)
        sql.append("""
        CREATE TABLE "statusreg" (
        "device_id" integer not null references "devices" ("id"), 
        "ts_value" datetime default (datetime('now','localtime'))
        );
        """)
        sql.append("""
        CREATE TABLE "rules" (
        "detail_id" integer not null references "devices" ("id"), 
        "value" integer not null,
        "ts_send" datetime default (datetime('now','localtime')) 
        );
        """)
        
        
        sql.append("""
        INSERT INTO "users" VALUES (NULL,"default","5f4dcc3b5aa765d61d8327deb882cf99","broken@email.addr");
        """)
                
        sql.append("""
         INSERT INTO "users" VALUES (NULL,"matt","5f4dcc3b5aa765d61d8327deb882cf99","matt@email.addr");
        """)
        for stmt in sql:
            self.exec_sql(stmt)
        
    def reinitDB(self):
        '''
            Drop all tables and re-initialize DB
        '''
        sql = []
        sql.append("""
        drop table if exists "devices";
        """)
        sql.append("""
        drop table if exists "details";
        """)
        sql.append("""
        drop table if exists "sessions";
        """)
        sql.append("""
        drop table if exists "users";
        """)
        sql.append("""
        drop table if exists "rules";
        """)
        sql.append("""
        drop table if exists "statusreg";
        """)
        for stmt in sql:
            self.exec_sql(stmt)
        '''
            Call the database creation function
        '''
        self.initDB()

    def initDevice(self, attrs):
        '''
            Create a device and seed config profile
        '''
        if attrs['DevType'] == 'arduino':
            sql = """INSERT INTO devices 
            (name, port, type, enabled) 
            VALUES 
            ('%s', '%s', '%s', '%s' )
            """ % (attrs['DevName'],attrs['DevPort'],attrs['DevType'], 1)
            self.exec_sql(sql)
            
            '''
                Get device ID by name
                Name should be unique 
                TODO: Add restriction for unique name with name check
                    
            '''
            
            sql = "select * from devices where name = '%s'" % attrs['DevName']
            result = self.query(sql)
            row = result.next()
            
            '''
                Seed pins 2 - 13
            '''
            for pin in range(2,14): 
                '''
                    Add Pins for Arduino
                    "ws_value" integer not null,
                    "hw_value" integer not null,
                    
                '''
                
                sql = """insert into  details 
                (device_id, label, config, pin, ws_value, hw_value, enabled)
                VALUES
                ('%s','%s','%s','%s','%s','%s', '%s')
                """ % (row['id'], 'default_'+str(pin), 0, pin, 0, 0 ,1)
                self.exec_sql(sql)
        
        '''
        ADD NEW DEVICE SETUP HERE
        #elif attrs['DevType'] == 'YOUR DEVICE TYPE':
        '''
        
       
    
    def query(self, sql):
        '''
            
        '''
        cursor = self.db.cursor()
        result = cursor.execute(sql)
        return result
    
    
    
    def exec_sql(self, sql):
        '''
            Perform inserts updates and deletes
            ACTIONS that do no require a return field
            
            ~Post Conditions~
                call commit on database.
        '''
        cursor = self.db.cursor()
        cursor.execute(sql)
        self.db.commit()
        
    def getPinByDid(self, DetailId):
        '''
            Get pin information using detail id 
        '''
        
        sql = "SELECT pin FROM details WHERE id = '%s'"  % (DetailId)
        '''
            Get the result from the database
        '''
        result = self.query(sql)
        '''
            Pass database row back to calling application
        '''
        pin = result.fetchone()[0]
        return pin

    def getDeviceById(self, DeviceId):
        '''
            Get device information using id 
        '''
        
        sql = "SELECT * from devices WHERE id = '%s'"  % (DeviceId)
        '''
            Get the result from the database
        '''
        result = self.query(sql)
        '''
            Pass database row back to calling application
        '''
        row = result.next()
        return row
            
        
    def getConfig(self, DetailId):
        '''
            Get device configuration information
            Pair down result set if DetailId is set
        '''
        sql = "SELECT pin, config FROM details "
        
        if DetailId:
            sql += " WHERE id = %s" % DetailId
            
        sql += " ORDER BY id asc"
        
        result = self.query(sql)
        return result
        
    def setDevice(self, dataset):
        '''
            Dataset is a dictionary of data elements device table
        '''
        sql = """INSERT INTO devices 
        (name, port, type, enabled) 
        VALUES 
        ('%s', '%s', '%s', '%s')""" % (dataset['name'], dataset['port'], dataset['type'], dataset['enabled'])
        self.exec_sql(sql)
   

# BEGIN JSON/HTML BACKEND SUPPORT

    def getLogin(self, username, password):
        ''' 
            Check Login Credentials
        '''
        pwdhash = hashlib.md5(password).hexdigest()
        sql = """SELECT COUNT(username) AS count
        FROM users 
        WHERE 
        username='%s'
        AND
        password='%s'
        """ % (username, pwdhash)
    
        ''' 
            Test to see if the database contains this record
            In this case a data dictionary is not requierd.
            So only test for a valid row returned from the database.
        '''
        result = self.query(sql)
        ''' 
           Get a single row from the database 
           Pass back a dictionary object for the row
        '''
        login = result.next()
    
        if login['count'] == 1:
            return True
        else:
            return False

    def getEmail(self, username):
        ''' 
            Get Email Address from Username
        '''
        sql = """SELECT email
        FROM users 
        WHERE 
        username='%s';
        """ % (username)
    
        result = self.query(sql)
        userinfo = result.next()
    
        return userinfo['email']


    def read(self):
	'''
		Retreive the current status of all enabled pins
	'''
        sql = """SELECT dev.id as did, det.id, det.label, dev.name, det.config,
			det.pin, det.hw_value as value, det.ws_ts as ts_value, det.ws_value, det.hw_ts, det.enabled as enabled  
		 FROM devices dev, details det
		 WHERE dev.id=det.device_id
		   AND dev.enabled=1;
        """
        result = self.query(sql)
	return result

    def changePin(self, did, value):
	'''
		Enable or disable a pin using the value provided
	'''
        setsql = """UPDATE details 
		 SET enabled=%s 
		 WHERE id=%s;
        """ % (value, did)

        self.exec_sql(setsql)

    def changeDevice(self, did, value):
	'''
		Enable or disable a device using the value provided
	'''
        setsql = """UPDATE devices 
		 SET enabled=%s 
		 WHERE id=%s;
        """ % (value, did)

        self.exec_sql(setsql)

    def setDetLabel(self, did, value):
	'''
		Set the label for a pin using the value provided
	'''
        setsql = """UPDATE details 
		 SET label='%s' 
		 WHERE id=%s;
        """ % (value, did)

        self.exec_sql(setsql)

    def setDevLabel(self, did, value):
	'''
		Set the label for a device using the value provided
	'''
        setsql = """UPDATE devices 
		 SET name='%s' 
		 WHERE id=%s;
        """ % (value, did)

        self.exec_sql(setsql)

    
    def write(self, did, value):
	'''
		Set a pins output to the value provided
	'''
        setsql = """UPDATE details 
		 SET ws_value=%s, ws_ts=datetime('now')
		 WHERE id=%s;
        """ % (value, did)

        self.exec_sql(setsql)

        sql = """SELECT ws_value
		 FROM details
		 WHERE id=%s;
        """ % (did)

        result = self.query(sql)
        current = result.next()

        if str(current['ws_value']) == str(value):
            return True
        else:
            return False

    def config(self, did, value):
	'''
		Set a pins configuration to the value provided
	'''
        setsql = """UPDATE details 
		 SET config=%s, ws_ts=datetime('now')
		 WHERE id=%s;
        """ % (value, did)

        self.exec_sql(setsql)

        sql = """SELECT config
		 FROM details
		 WHERE id=%s;
        """ % (did)

        result = self.query(sql)
        current = result.next()

        if str(current['config']) == str(value):
            return True
        else:
            return False

