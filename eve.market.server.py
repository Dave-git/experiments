import urlparse as urlparse
import urllib as urllib
import sqlite3 as SQL
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from xml.etree import ElementTree as ET
import requests as req
import os



PORT_NUMBER = 8080



regionlist = {'Derelik':10000001,'The Forge':10000002,'Vale of the Silent':10000003,'UUA-F4':10000004,'Detorid':10000005,'Wicked Creek':10000006,'Cache':10000007,'Scalding Pass':10000008,'Insmother':10000009,'Tribute':10000010,'Great Wildlands':10000011,'Curse':10000012,'Malpais':10000013,'Catch':10000014,'Venal':10000015,'Lonetrek':10000016,'J7HZ-F':10000017,'The Spire':10000018,'A821-A':10000019,'Tash-Murkon':10000020,'Outer Passage':10000021,'Stain':10000022,'Pure Blind':10000023,'Immensea':10000025,'Etherium Reach':10000027,'Molden Heath':10000028,'Geminate':10000029,'Heimatar':10000030,'Impass':10000031,'Sinq Laison':10000032,'The Citadel':10000033,'The Kalevala Expanse':10000034,'Deklein':10000035,'Devoid':10000036,'Everyshore':10000037,'The Bleak Lands':10000038,'Esoteria':10000039,'Oasa':10000040,'Syndicate':10000041,'Metropolis':10000042,'Domain':10000043,'Solitude':10000044,'Tenal':10000045,'Fade':10000046,'Providence':10000047,'Placid':10000048,'Khanid':10000049,'Querious':10000050,'Cloud Ring':10000051,'Kador':10000052,'Cobalt Edge':10000053,'Aridia':10000054,'Branch':10000055,'Feythabolis':10000056,'Outer Ring':10000057,'Fountain':10000058,'Paragon Soul':10000059,'Delve':10000060,'Tenerifis':10000061,'Omist':10000062,'Period Basis':10000063,'Essence':10000064,'Kor-Azor':10000065,'Perrigen Falls':10000066,'Genesis':10000067,'Verge Vendor':10000068,'Black Rise':10000069}


def quicklook(arg):
     '''formats data from the quicklook api call into dictionaries.  
     Returns a tuple with item 0 = sell and item 1 = buy'''
     from functools import wraps
     dict_resp = {}
     @wraps(arg)
     
     def wrapper(*args):
          #sell = {}
          #buy = {}
          order = {}
	  tempdb = 'temp.db'
	  conn = SQL.connect(tempdb)
	  conn.text_factory = str
	  cur = conn.cursor()	  
          xml = ET.fromstring(arg(*args))
	  
          for node in xml.iter():
               if node.tag == 'sell_orders':
                    for sellorders in node.iter():
                         if sellorders.tag == 'order':
                              for orders in sellorders.iter():
                                   order[orders.tag] = orders.text
                              #sell[sellorders.attrib['id']] = order
			      cur.execute('''INSERT INTO tempmarketdata VALUES (?,?,?,?,?,?,?,?)''',(urlcheck['typeid'], 'sell', order['expires'], order['security'], order['vol_remain'], order['region'], order['station'], order['station_name']))
			      conn.commit()
                              order = {}
                              
               elif node.tag == 'buy_orders':
                    for buyorders in node.iter():
                         if buyorders.tag == 'order':
                              for orders in buyorders.iter():
                                   order[orders.tag] = orders.text
                              #buy[buyorders.attrib['id']] = order
			      cur.execute('''INSERT INTO tempmarketdata VALUES (?,?,?,?,?,?,?,?)''',(urlcheck['typeid'], 'buy', order['expires'], order['security'], order['vol_remain'], order['region'], order['station'], order['station_name']))
			      conn.commit()
                              order = {}
			      
	  conn.close()
          
     return wrapper

def parsepath(url):
     decodedurl = urllib.unquote(url)
     parsedurl = urlparse.urlparse(decodedurl)		
     #path = checkpath(parsedurl.path)
     rawquery = urlparse.parse_qsl(parsedurl.query)
     query = checkquery(rawquery)
     #print rawquery
     if parsedurl.path == '/' and rawquery == []:
	  return {'status':200}	  
     elif query['status'] != 200:
	  return query
     else:
	  return {'status':200, 'typeid':query['typeid'], 'typename':query['typename'], 'minquantity':query['minquantity'], 'security':query['security']} 
	    
def checkquery(rv_query):
     '''Function to check query parameters.  Either returns extracted values as a dictionary or returns error'''
     security = 0
     minquantity = 0
     if len(rv_query) !=3:
	  return {'status':400, 'ErrorText':'Incorrect number of specified query parameters "{0}" and 3 are expected'.format(len(rv_query))}
	    
     for i in rv_query:
	  if i[0] == 'sec':
	       security = i[1]
	  elif i[0] == 'minQ':
	       minquantity = i[1]
	  elif i[0] == 'typename':
	       conn = SQL.connect('eve_dump.db')
	       conn.text_factory = str
	       cur = conn.cursor()
	       sqlobj = cur.execute('SELECT typeid FROM typeid WHERE type=?',(i[1],))
	       rv = sqlobj.fetchone()
	       if rv == None:
		    conn.close()
		    return {'status':404, 'ErrorText':'File not found: {0} not recognised'.format(i[1])}
	       else:
		    conn.close()
		    typename =i[0]
		    typeid = rv[0]	       
	  else:
	       return {'status':400, 'ErrorText':'One or query parameters "{0}" is not understood'.format(i[0])}
	    
     return {'status':200,'security':security, 'minquantity':minquantity, 'typename':typename, 'typeid':typeid}

@quicklook
def queryquicklook(typeid, regionid, minquantity):
     payload = {'typeid':typeid, 'regionlimit':regionid, 'setminQ':minquantity}
     rv = req.get('http://api.eve-central.com/api/quicklook', params=payload)
     return rv.text

def presenter(url):
     global urlcheck
     tempdb = 'temp.db'
     urlcheck = parsepath(url)
     if urlcheck['status'] != 200:
	  return {'status':urlcheck['status'],'responsetext':'<html><b>Error {0}:</b> {1}</html>'.format(urlcheck['status'],urlcheck['ErrorText'])}
     if urlcheck['status'] == 200 and len(urlcheck) <= 1:
	  with open('index.html') as f:
	       responsetext = f.read()
	  return {'status':200,'responsetext':responsetext}
     if urlcheck['status'] == 200 and len(urlcheck) >= 2:

	  conn = SQL.connect(tempdb)
	  conn.text_factory = str
	  cur = conn.cursor()
	  check = cur.execute('''SELECT COUNT(*) from tempmarketdata WHERE typeid = ?''',(str(urlcheck['typeid']),))
	  annoy = check.fetchone()
	  
	  conn.close()
	  if annoy[0] == 0:
	       
	       for region in regionlist:
		    queryquicklook(urlcheck['typeid'], regionlist[region], urlcheck['minquantity'])

	  conn = SQL.connect(tempdb)
	  conn.text_factory = str
	  cur = conn.cursor()	  
	  outstuff = cur.execute('''SELECT * from tempmarketdata WHERE security>=? AND typeid =? AND vol_remain >=?''',(urlcheck['security'], urlcheck['typeid'], urlcheck['minquantity']))
	  responset = outstuff.fetchall()
	  conn.close()
	  return {'status':urlcheck['status'],'responsetext':'<html><font face="verdana" size="2">{0}</font></html>'.format(responset, )}
     
class myHandler(BaseHTTPRequestHandler):
     #Handler for the GET requests
     def do_GET(self):
	  self.response = presenter(self.path)
	  self.send_response(self.response['status'])
	  self.send_header('Content-type','text/html')
	  self.end_headers()
	  self.wfile.write(self.response['responsetext'])
	  #return
	  
try:
     #Create a web server and define the handler to manage the
     #incoming request
     print 'Setting up temporary database.  Be patient.'
     tempdb = 'temp.db'
     conn = SQL.connect(tempdb)
     conn.text_factory = str
     cur = conn.cursor()
     cur.execute('''DROP table if exists tempmarketdata''')
     cur.execute('''CREATE TABLE tempmarketdata(typeid, ordertype, expires, security, vol_remain, region, station, station_name)''')
     conn.close()
     print 'done'
	  
     server = HTTPServer(('', PORT_NUMBER), myHandler)
     print 'Started httpserver on port ' , PORT_NUMBER
		  
     #Wait forever for incoming htto requests
     server.serve_forever()
	  
except KeyboardInterrupt:
     print '^C received, shutting down the web server'
     tempdb = 'temp.db'
     conn = SQL.connect(tempdb)
     cur = conn.cursor()
     cur.execute('''DROP table if exists tempmarketdata''')
     conn.commit()
     conn.close()
     server.socket.close() 

