#import the web py module import web
import hashlib
import web
#from web import form
import sqlite3
import datetime

#import the CherryPy server with ssl support
#from web.wsgiserver import CherryPyWSGIServer

#define the ssl cert and key, yes these are self signed
#CherryPyWSGIServer.ssl_certificate = "ssl.key/csu_hrc51_com.crt"
#CherryPyWSGIServer.ssl_private_key = "ssl.key/csu_hrc51_com.key"

#define database stuff
db = web.database(dbn='sqlite', db='andruino.db')

urls  = ("/", "index")
urls += ("/login", "login")
urls += ("/logout", "logout")
urls += ("/sqlts", "sqlts")
urls += ("/config", "config")
urls += ("/devdetails", "devdetails")
urls += ("/adddevice", "adddevice")
urls += ("/adddetails", "adddetails")
urls += ("/read", "read")
urls += ("/write", "write")

app = web.application(urls, globals())
render = web.template.render('json/')

if web.config.get('_session') is None:
	store = web.session.DBStore(db, 'sessions')
	session = web.session.Session(app, store)
	web.config._session = session
else:
	session = web.config._session


class index:
	def GET(self):
		return '{"command":"index","response":"Hello, World!"}'

class login:
	def POST(self):
		wi = web.input()
		pwdhash = hashlib.md5(wi.password).hexdigest()
		dbQuery = "SELECT username, email FROM users \
		WHERE username='"+wi.username+"' AND password='"+pwdhash+"';"
		check = db.query(dbQuery)
		try:
			session.username = wi.username
			session.email = check[0].email
			session.loggedin = True
			return '{"command":"login","response":"pass"}'
		except:
			session.loggedin = False
			return '{"command":"login","response":"fail"}'

class logout:
	def GET(self):
		session.kill()
		return '{"command":"logout","response":"bye!"}'

class sqlts:
	def GET(self):
		dbQuery = "SELECT DATETIME('now') AS now;"
		dbts = db.query(dbQuery)
		return '{"command":"sqlts","response":"'+dbts[0].now+'"}'

class config:
	def GET(self):
		try: session.username
		except AttributeError: '{"command":"write","response":"auth"}'
		deviceList = db.select('devices')
		return render.devices("Device List", deviceList)

class devdetails:
	def GET(self):
		try: session.username
		except AttributeError: '{"command":"write","response":"auth"}'
		myvar = web.input()
		detailList = db.select('details', myvar, where="device_id = $device_id")
		return render.details("Device Details", detailList)

class read:
	def GET(self):
		#try: session.username
		#except AttributeError: '[{"command":"write","response":"auth"}]'
		dbQuery = 'SELECT dev.id as did, det.id, det.label, dev.name, det.ddr,\
		 det.pin, det.value, det.ts_value FROM devices dev, details det\
		 WHERE dev.id=det.device_id AND dev.enabled=1 AND det.enabled=1;'
		statuses = db.query(dbQuery)

		responseList = list()
		for status in statuses:
			response = '{"did":"'+str(status['did'])+'",'
			response += '"id":"'+str(status['id'])+'",'
			response += '"label":"'+str(status['label'])+'",'
			response += '"device":"'+str(status['name'])+'",'
			response += '"ddr":"'+str(status['ddr'])+'",'
			response += '"pin":"'+str(status['pin'])+'",'
			response += '"value":"'+str(status['value'])+'",'
			response += '"ts_value":"'+str(status['ts_value'])+'"}'
			responseList.append(response)
		return '{"command":"read","response":"'+str(len(responseList))+'","details":['+",".join(responseList)+']}'

class write:
	def GET(self):
		try: session.username
		except AttributeError: '[{"command":"write","response":"auth"}]'
		myvar = web.input()
		dbQuery = "UPDATE details SET value = '"+myvar['value']+"', last_value = '"+myvar['value']+"', ts_value=datetime('now'), ts_output=datetime('now') WHERE id = '"+myvar['did']+"'"
		result = db.query(dbQuery)
		if result:
			return '[{"command":"write","response":"done"}]'
		else:
			return '[{"command":"write","response":"fail"}]'

class adddevice:
	def GET(self):
		try: session.username
		except AttributeError: '[{"command":"write","response":"auth"}]'
		f = adddevice_form()
		return render.adddevice(f)

	def POST(self):
		try: session.username
		except AttributeError: '[{"command":"write","response":"auth"}]'
		f = adddevice_form()
		if not f.validates():
			return render.adddevice(f)
		else:
			return db.insert('devices', **f.d)

class adddetails:
	def GET(self):
		try: session.username
		except AttributeError: '[{"command":"write","response":"auth"}]'
		myvar = web.input(device_id='0')
		device = db.select('devices', myvar, where="id = $device_id")
		details = db.select('details', myvar, where="device_id = $device_id")
		f = adddetails_form()
		return render.adddetails(f,device,details)

	def POST(self):
		try: session.username
		except AttributeError: '[{"command":"write","response":"auth"}]'
		myvar = web.input(device_id='0')
		f = adddetails_form()
		if not f.validates():
			return render.adddetails(f)
		else:
			db.insert('details', **f.d)
			raise web.seeother('/adddetails?device_id='+myvar['device_id'])

if __name__ == "__main__":
	app.run()
