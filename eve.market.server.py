import urlparse as urlparse
import urllib as urllib
import sqlite3 as SQL
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from xml.etree import ElementTree as ET
import requests as req
PORT_NUMBER = 8080

regionlist = {'Derelik':10000001,'The Forge':10000002,'Vale of the Silent':10000003,'UUA-F4':10000004,'Detorid':10000005,'Wicked Creek':10000006,'Cache':10000007,'Scalding Pass':10000008,'Insmother':10000009,'Tribute':10000010,'Great Wildlands':10000011,'Curse':10000012,'Malpais':10000013,'Catch':10000014,'Venal':10000015,'Lonetrek':10000016,'J7HZ-F':10000017,'The Spire':10000018,'A821-A':10000019,'Tash-Murkon':10000020,'Outer Passage':10000021,'Stain':10000022,'Pure Blind':10000023,'Immensea':10000025,'Etherium Reach':10000027,'Molden Heath':10000028,'Geminate':10000029,'Heimatar':10000030,'Impass':10000031,'Sinq Laison':10000032,'The Citadel':10000033,'The Kalevala Expanse':10000034,'Deklein':10000035,'Devoid':10000036,'Everyshore':10000037,'The Bleak Lands':10000038,'Esoteria':10000039,'Oasa':10000040,'Syndicate':10000041,'Metropolis':10000042,'Domain':10000043,'Solitude':10000044,'Tenal':10000045,'Fade':10000046,'Providence':10000047,'Placid':10000048,'Khanid':10000049,'Querious':10000050,'Cloud Ring':10000051,'Kador':10000052,'Cobalt Edge':10000053,'Aridia':10000054,'Branch':10000055,'Feythabolis':10000056,'Outer Ring':10000057,'Fountain':10000058,'Paragon Soul':10000059,'Delve':10000060,'Tenerifis':10000061,'Omist':10000062,'Period Basis':10000063,'Essence':10000064,'Kor-Azor':10000065,'Perrigen Falls':10000066,'Genesis':10000067,'Verge Vendor':10000068,'Black Rise':10000069}

def hiseconly(orders, security):
     '''removes orders below a given security'''
     for x in orders.keys():
          if float(orders[x]['security']) < security:
               del orders[x]
     return orders

def maxprice(orders):
     '''returns the highest price for orders with a significant volume remaining'''
     max_price = 0
     max_order = {}

     for x in orders.keys():
          if float(orders[x]['price']) < max_price:
	       pass
          else:
               max_order = orders[x]
               max_price = orders[x]['price']
          
     return max_order

def minprice(orders):
     '''returns the highest price for orders with a significant volume remaining'''
     min_price = 9999999999
     min_order = {}

     for x in orders.keys():
          if float(orders[x]['price']) > min_price:
	       pass
          else:
               min_order = orders[x]
               min_price = orders[x]['price']
               
     return min_order

def quicklook(arg):
     '''formats data from the quicklook api call into dictionaries.  
     Returns a tuple with item 0 = sell and item 1 = buy'''
     from functools import wraps
     dict_resp = {}
     @wraps(arg)
     
     def wrapper(*args):
          sell = {}
          buy = {}
          order = {}
          xml = ET.fromstring(arg(*args))
          for node in xml.iter():
               if node.tag == 'sell_orders':
                    for sellorders in node.iter():
                         if sellorders.tag == 'order':
                              for orders in sellorders.iter():
                                   order[orders.tag] = orders.text
                              sell[sellorders.attrib['id']] = order
                              order = {}
                              
               elif node.tag == 'buy_orders':
                    for buyorders in node.iter():
                         if buyorders.tag == 'order':
                              for orders in buyorders.iter():
                                   order[orders.tag] = orders.text
                              buy[buyorders.attrib['id']] = order
                              order = {}            
                    
                    
          return sell, buy
     return wrapper

def parsepath(url):
     decodedurl = urllib.unquote(url)
     parsedurl = urlparse.urlparse(decodedurl)		
     path = checkpath(parsedurl.path)
     query = checkquery(urlparse.parse_qsl(parsedurl.query))
     if query['status'] != 200:
	  return query
     elif path['status'] != 200:
	  return path
     else:
	  return {'status':200, 'typeid':path['typeid'], 'typename':path['typename'], 'minquantity':query['minquantity'], 'security':query['security']}

def checkpath(strpath):
     returnvalue = {}
     rv_path = strpath[1:].split('/')
     for i in range(len(rv_path)):
	  if rv_path[i] == '':
	       del rv_path[i]	    
	  if len(rv_path) !=1:
	       return {'status':400, 'ErrorText':'Incorrect number of "path" parameters: {0} supplied only 1 is expected'.format(len(rv_path))}	
	  else:
	       conn = SQL.connect('eve_dump.db')
	       conn.text_factory = str
	       cur = conn.cursor()
	       sqlobj = cur.execute('SELECT typeid FROM typeid WHERE type=?',(rv_path[0],))
	       rv = sqlobj.fetchone()
	       if rv == None:
		    conn.close()
		    return {'status':404, 'ErrorText':'File not found: {0} not recognised'.format(rv_path[0])}
	       else:
		    conn.close()
		    return {'status':200, 'typename':rv_path[0], 'typeid':rv[0]}
	    
def checkquery(rv_query):
     '''Function to check query parameters.  Either returns extracted values as a dictionary or returns error'''
     security = 0
     minquantity = 0
     if len(rv_query) !=2:
	  return {'status':400, 'ErrorText':'Incorrect number of specified query parameters "{0}" and 2 are expected'.format(len(rv_query))}
	    
     for i in rv_query:
	  if i[0] == 'sec':
	       security = i[1]
	  elif i[0] == 'minQ':
	       minquantity = i[1]
	  else:
	       return {'status':400, 'ErrorText':'One or query parameters "{0}" is not understood'.format(i[0])}
	    
     return {'status':200,'security':security, 'minquantity':minquantity}

@quicklook
def queryquicklook(typeid, regionid, minquantity):
     payload = {'typeid':typeid, 'regionlimit':regionid, 'setminQ':minquantity}
     rv = req.get('http://api.eve-central.com/api/quicklook', params=payload)
     return rv.text

def presenter(url):
     sell = []
     buy = []
     buyercount = 0
     salecount = 9999999999     
     urlcheck = parsepath(url)
     if urlcheck['status'] != 200:
	  return {'status':urlcheck['status'],'responsetext':'<html><b>Error {0}:</b> {1}</html>'.format(urlcheck['status'],urlcheck['ErrorText'])}
     
     if urlcheck['status'] == 200:
	  for region in regionlist:
	       more = queryquicklook(urlcheck['typeid'], regionlist[region], urlcheck['minquantity'])

	       sellsec = hiseconly(more[0],float(urlcheck['security']))
	       buysec = hiseconly(more[1],float(urlcheck['security']))
	       sale = minprice(sellsec)
	       buyer = maxprice(buysec)
	       if sale !={} and float(sale['price']) < salecount:
		    salecount = float(sale['price'])
		    sell = sale
     
	       if buyer != {} and float(buyer['price']) > buyercount:
		    buyercount = float(buyer['price'])
		    buy = buyer
	  
	  responsesell = '<tr><td>{0}</td><td>{1}</td><td>{2}</td></tr>'.format(sell['price'], sell['vol_remain'], sell['station_name'])
	  responsebuy = '<tr><td>{0}</td><td>{1}</td><td>{2}</td></tr>'.format(buy['price'], buy['vol_remain'], buy['station_name'])
	  return {'status':urlcheck['status'],'responsetext':'<html><table><tr><th>price</th><th>vol_remain</th><th>station_name</th></tr>{0}{1}</table></html>'.format(responsesell, responsebuy)}
     
     
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
     server = HTTPServer(('', PORT_NUMBER), myHandler)
     print 'Started httpserver on port ' , PORT_NUMBER
	     
     #Wait forever for incoming htto requests
     server.serve_forever()
     
except KeyboardInterrupt:
     print '^C received, shutting down the web server'
     server.socket.close()

#if __name__=="__main__":
     
     #print presenter('http://localhost:8080/Pyerite?sec=0.5&minQ=2000')
     

