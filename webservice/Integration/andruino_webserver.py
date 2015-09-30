import cherrypy
from andruino_db import *
from andruino_api import *
import time
import os, sys
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
			response += '"ts_value":"'+str(status['ts_value'])+'",'
			response += '"enabled":"'+str(status['enabled'])+'"}'
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

class Enable:
	'''
	_cp_config = { 
		'tools.session_auth.on': True, 
		'tools.session_auth.login_screen' : requireLogin,
	} 
	'''
	@cherrypy.expose
	def pin(self,did):
		AnDB.changePin(did,1)
		return '{"command":"enable","response":"pass"}'
	def device(self,did):
		AnDB.changeDevice(did,1)
		return '{"command":"enable","response":"pass"}'

class Disable:
	'''
	_cp_config = { 
		'tools.session_auth.on': True, 
		'tools.session_auth.login_screen' : requireLogin,
	} 
	'''
	@cherrypy.expose
	def pin(self,did):
		AnDB.changePin(did,0)
		return '{"command":"disable","response":"pass"}'
	def device(self,did):
		AnDB.changeDevice(did,0)
		return '{"command":"disable","response":"pass"}'

class SetLabel:
	'''
	_cp_config = { 
		'tools.session_auth.on': True, 
		'tools.session_auth.login_screen' : requireLogin,
	} 
	'''
	@cherrypy.expose
	def pin(self,did,label):
		AnDB.setDetLabel(did,label)
		return '{"command":"setlabel","response":"pass"}'
	def device(self,did,label):
		AnDB.setDevLabel(did,label)
		return '{"command":"setlabel","response":"pass"}'

class Exit:
	'''
	_cp_config = { 
		'tools.session_auth.on': True, 
		'tools.session_auth.login_screen' : requireLogin,
	} 
	'''
	@cherrypy.expose
	def default(self):
		Api.stopSerial()
		sys.exit()


if __name__ == '__main__':

	root = Root()
	root.login = Login()
	root.logout = Logout()
	root.userinfo = UserInfo()
	root.read = Read()
	root.write = Write()
	root.config = Config()
	root.enable = Enable()
	root.disable = Disable()
	root.setlabel = SetLabel()
	root.exit = Exit()


	Api.startSerial()
	cherrypy.server.socket_host = '0.0.0.0'
	cherrypy.config.update({'tools.sessions.on' : True})
	cherrypy.quickstart(root)
	print "------ STOP THREADS ---------"
	'''
		Stop any threads that have started...
	'''
	
	
	Api.stopSerial()

