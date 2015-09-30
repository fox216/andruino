import cherrypy
from andruino_db import *
from andruino_api import *
import time
#import os
#from tempfile import gettempdir

#import sys, os
#import datetime
#from struct import *
#from andruino_api import *

AnDB = AndruinoDb()
'''
	Initial version of the andruino application will only 
	support a single device...
	Future releases will add Multiple device support
	
	For configuration purposes, Manually set DeviceId to reference database ID
'''
Api = AndruinoApi(DeviceId=1)


def requireLogin(self): 
		return '{"command":"login","response":"fail"}'

class Root:
	@cherrypy.expose
	def index(self):
		return '{"command":"index","response":"Hello, World!"}'


class Login:
	@cherrypy.expose
	def default(self,username,password):
		if (AnDB.getLogin(username,password)):
			cherrypy.session['username'] = username
			cherrypy.session['email'] = AnDB.getEmail(username)
			cherrypy.session['loggedin'] = True
			return '{"command":"login","response":"pass"}'
		else:
			cherrypy.session['loggedin'] = False
			return '{"command":"login","response":"fail"}'

class Logout:
	'''
	_cp_config = { 
		'tools.session_auth.on': True, 
		'tools.session_auth.login_screen' : requireLogin,
	} 
	'''
	@cherrypy.expose
	def default(self):
		cherrypy.session['username'] = ""
		cherrypy.session['email'] = ""
		cherrypy.session['loggedin'] = False
		return '{"command":"logout","response":"pass"}'


class UserInfo:
	'''
	_cp_config = { 
		'tools.session_auth.on': True, 
		'tools.session_auth.login_screen' : requireLogin,
	} 
	'''
	@cherrypy.expose
	def default(self):
		if (cherrypy.session.get('loggedin')):
			return '{"command":"userinfo","response":"loggedin","userinfo":[{'\
				+'"username":"'+cherrypy.session.get('username')\
				+'","email":"'+cherrypy.session.get('email')\
				+'"}]}'
		else:
			return '{"command":"userinfo","response":"loggedout"}'


class Read:
	#_cp_config = { 
		#'tools.session_auth.on': True, 
		#'tools.session_auth.login_screen' : requireLogin,
	#} 
	@cherrypy.expose
	def default(self):
		statuses = AnDB.read()
		responseList = list()
		for status in statuses:
			response = '{"did":"'+str(status['did'])+'",'
			response += '"id":"'+str(status['id'])+'",'
			response += '"label":"'+str(status['label'])+'",'
			response += '"device":"'+str(status['name'])+'",'
			response += '"ddr":"'+str(status['config'])+'",'
			response += '"pin":"'+str(status['pin'])+'",'
			response += '"value":"'+str(status['value'])+'",'
			response += '"ts_value":"'+str(status['ts_value'])+'"}'
			responseList.append(response)
		return '{"command":"read","response":"'+str(len(responseList))+'","details":['\
			+",".join(responseList)+']}'


class Write:
	'''
	_cp_config = { 
		'tools.session_auth.on': True, 
		'tools.session_auth.login_screen' : requireLogin,
	} 
	'''
	@cherrypy.expose
	def default(self,did,value):
		'''
			Write to device 
			TODO: This is a stop gap.
			Update will change to data lifecycle this is a 
			short term fix for demonstration purposes 
		'''
		Api.writeOutput(did,value)
		if (AnDB.write(did,value)):
			return '{"command":"write","response":"pass"}'
		else:
			return '{"command":"write","response":"fail"}'
		

class Config:
	'''
	_cp_config = { 
		'tools.session_auth.on': True, 
		'tools.session_auth.login_screen' : requireLogin,
	} 
	'''
	@cherrypy.expose
	def default(self,did,value):
		if (AnDB.config(did,value)):
			Api.writeConfig(did)
			return '{"command":"config","response":"pass"}'
		else:
			return '{"command":"config","response":"fail"}'
		'''
			Write config to device
			1) read config from database
			2) set device
			
			TODO: This is a stop gap.
			Update will change to data lifecycle this is a 
			short term fix for demonstration purposes 
		'''
		


class Admin:
	'''
	_cp_config = { 
		'tools.session_auth.on': True, 
		'tools.session_auth.login_screen' : requireLogin,
	} 
	'''
	

	
	@cherrypy.expose
	def index(self, screen=None):
		if not screen:
			'''
				Display default form...
			'''
			return """
<html>
<form action="initDb" method="post">
	<fieldset>
	<legend>Database Setup</legend>
	<a href=/admin?screen=seed>Device Setup</a><br>
	<a href=/admin?screen=control>Device Control</a><br>
	<br>
	<input type='radio' name='dbcmd' value='initdb' /><label>Initialize Database</lable><br>
	<input type='radio' name='dbcmd' value='reinitdb' /><label>Re-Initialize Database</lable><br>
	<input type='submit'>
	
	</fieldset>	
</form>
</html>		
"""
		elif screen == 'seed':
			'''
				Display the seeding ooptions
			'''
			return """
<form action="initDev" method="post">
	<fieldset>
	<legend>AVR Device Type</legend>
	<a href=/admin>Database Init</a><br>
	<a href=/admin?screen=control>Device Control</a><br>
	<br>
	<input type='radio' name='devtype' value='arduino' /><label>Arduino</lable><br>
	<input type='radio' name='devtype' value='mega'  disabled='true'/><label>AVR Mega</lable><br>
	<label>Device Name:</lable> <input type='text' name='devname' size='40'/><br>
	<label>Port:</lable> <input type='text' name='devport' size='40'/><br>
	
	
	<input type='submit'>
	
	</fieldset>	
</form>
</html>	
"""
		elif screen == 'control':
			return """
<html>
<form action="devCtrl" method="post">
	<fieldset>
	<legend>Database Setup</legend>
	<a href=/admin>Database Init</a><br>
	<a href=/admin?screen=seed>Device Setup</a><br>
	<br>
	<input type='radio' name='ctrl' value='start' /><label>Start Device</lable><br>
	<input type='radio' name='ctrl' value='stop' /><label>Stop Device</lable><br>
	<input type='submit'>
	
	</fieldset>	
</form>
</html>		
"""
		elif screen == 'config':
			return """
<html>
<form action="devCfg" method="post">
	<fieldset>
	<legend>Database Setup</legend>
	<a href=/admin>Database Init</a><br>
	<a href=/admin?screen=seed>Device Setup</a><br>
	<br>
	<input type='radio' name='ctrl' value='0' /><label>Input</lable><br>
	<input type='radio' name='ctrl' value='1' /><label>Output</lable><br>
	<label>Pin:</lable> <input type='text' name='pin' size='4'/><br>
	<input type='submit'>
	
	</fieldset>	
</form>
</html>		
"""

						
	def initDb(self, dbcmd=None):
		'''
			 Perform db operations using api
		'''
		
		if dbcmd == 'initdb':
			'''
				Init db
			'''
			AnDB.initDB()
			return """Initial Database created """
		elif dbcmd == 'reinitdb':
			'''
				Reinit db
			'''
			AnDB.reinitDB()
			return """Database Re-initialization Complete """
			
		
	initDb.exposed = True
	
	def initDev(self, devtype=None, devname=None, devport=None):
		'''
			 Perform db operations using api
		'''
		devAttr = {'DevName': devname, 'DevType': devtype, 'DevPort': devport}
		AnDB.initDevice(devAttr)
	initDev.exposed = True
	
	def devCtrl(self, ctrl=None):
		'''
			 
		'''
		if ctrl == 'start':
			'''
				Start the device thread
			'''
			Api.startSerial()
			
		elif ctrl == 'stop':
			'''
				Stop the device thread
			'''
			Api.stopSerial()
			
		
	devCtrl.exposed = True
		

if __name__ == '__main__':

	root = Root()
	root.login = Login()
	root.logout = Logout()
	root.userinfo = UserInfo()
	root.read = Read()
	root.write = Write()
	root.admin = Admin()
	
	root.config = Config()
	
	
	
	
	
	
	
	'''
		Start the API
		
	'''
	#Api.startSerial()
	#http://docs.cherrypy.org/dev/refman/process/plugins/index.html
	
	cherrypy.server.socket_host = '0.0.0.0'
	cherrypy.config.update({'tools.sessions.on' : True})
	cherrypy.quickstart(root)
	print "------ STOP THREADS ---------"
	'''
		Stop any threads that have started...
	'''
	Api.stopSerial()
	
	
		
		
