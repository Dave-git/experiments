import requests as req
from xml.etree import ElementTree as ET
from HTMLParser import HTMLParser
import json as json

regionid = {'Derelik':10000001,'The Forge':10000002,'Vale of the Silent':10000003,'UUA-F4':10000004,'Detorid':10000005,'Wicked Creek':10000006,'Cache':10000007,'Scalding Pass':10000008,'Insmother':10000009,'Tribute':10000010,'Great Wildlands':10000011,'Curse':10000012,'Malpais':10000013,'Catch':10000014,'Venal':10000015,'Lonetrek':10000016,'J7HZ-F':10000017,'The Spire':10000018,'A821-A':10000019,'Tash-Murkon':10000020,'Outer Passage':10000021,'Stain':10000022,'Pure Blind':10000023,'Immensea':10000025,'Etherium Reach':10000027,'Molden Heath':10000028,'Geminate':10000029,'Heimatar':10000030,'Impass':10000031,'Sinq Laison':10000032,'The Citadel':10000033,'The Kalevala Expanse':10000034,'Deklein':10000035,'Devoid':10000036,'Everyshore':10000037,'The Bleak Lands':10000038,'Esoteria':10000039,'Oasa':10000040,'Syndicate':10000041,'Metropolis':10000042,'Domain':10000043,'Solitude':10000044,'Tenal':10000045,'Fade':10000046,'Providence':10000047,'Placid':10000048,'Khanid':10000049,'Querious':10000050,'Cloud Ring':10000051,'Kador':10000052,'Cobalt Edge':10000053,'Aridia':10000054,'Branch':10000055,'Feythabolis':10000056,'Outer Ring':10000057,'Fountain':10000058,'Paragon Soul':10000059,'Delve':10000060,'Tenerifis':10000061,'Omist':10000062,'Period Basis':10000063,'Essence':10000064,'Kor-Azor':10000065,'Perrigen Falls':10000066,'Genesis':10000067,'Verge Vendor':10000068,'Black Rise':10000069}





def numberjumpsroute(start, finish):
     path = 'http://api.eve-central.com/api/route/from/{0}/to/{1}'.format(start,finish)
     rv = req.get(path)
     return len(rv.json())

def getstations(url):
     rv = req.get(url)
     return rv.text

def evapi(arg):
     from functools import wraps
     charID = 0
     @wraps(arg)
     def wrapper(*args):
          xml = ET.fromstring(arg(*args))
          for node in xml.iter():
               if node.tag == 'row':
                    charID = node.attrib['characterID']
          return charID
     return wrapper
     
     

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

def marketstat(arg):
     '''formats data from the marketstat api call into dictionaries'''
     from functools import wraps
     dict_resp = {}
     @wraps(arg)
     
     def wrapper(*args):
          sell = {}
          buy = {}
          xml = ET.fromstring(arg(*args))
          for node in xml.iter():
               if node.tag == 'sell':
                    for subnode in node.iter():
                         if subnode.text != None:
                              sell[subnode.tag] = subnode.text
                         else:
                              sell[subnode.tag] = str(*args)
               elif node.tag == 'buy':
                    for subnode in node.iter():
                         if subnode.text != None:
                              buy[subnode.tag] = subnode.text
                         else:
                              buy[subnode.tag] = str(*args)                    
                    
                    
          return sell, buy
     return wrapper

def profit(buyvol, sellmin, buymax):
     
     return (float(buyvol) * (float(buymax)-float(sellmin)))

@evapi
def eveid(objectname):
     path = 'https://api.eveonline.com/eve/CharacterID.xml.aspx'
     payload = {'names':objectname}
     rv = req.get(path, params=payload)
     return rv.text    

@marketstat
def querymarketstat(name):
     '''requests data from the marketstat endpoint'''
     typeid={'Tritanium':34, 'Pyerite':35}
     payload = {'typeid':typeid[name]}
     rv = req.get('http://api.eve-central.com/api/marketstat', params=payload)
     return rv.text

@quicklook
def queryquicklook(name, region, minquantity):
     '''requests data from the quicklook endpoint'''
     typeid={'Tritanium':34, 'Pyerite':35}
     payload = {'typeid':typeid[name], 'regionlimit':regionid[region], 'setminQ':minquantity}
     rv = req.get('http://api.eve-central.com/api/quicklook', params=payload)
     return rv.text


def lowerlimit(orders, minprice):
     '''removes orders above a given price'''
     for x in orders.keys():
          if float(orders[x]['price']) >= minprice:
               del orders[x]
     return orders


def upperlimit(orders, maxprice):
     '''removes orders below a given price'''
     for x in orders.keys():
          if float(orders[x]['price']) <= maxprice:
               del orders[x]
     return orders

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
               #del orders[x]
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
               #del orders[x]
               pass
          else:
               min_order = orders[x]
               min_price = orders[x]['price']
               
     return min_order


                    
     

if __name__=="__main__":
     
     sell = []
     buy = []
     #data = querymarketstat('Tritanium')
     #tritanium_heimatar = queryquicklook('Tritanium', 'Heimatar')
     #tritanium_SinqLaison = queryquicklook('Tritanium', 'Sinq Laison')
     #tritanium_TheForge = queryquicklook('Tritanium', 'The Forge', 20000)
     #print tritanium_TheForge[0]
     #print(minimum(tritanium_heimatar[0],1000), 'mini sell')
     #print(maximum(tritanium_heimatar[1],1000), 'maxi buy')
     #print(minimum(tritanium_SinqLaison[0],1000), 'mini sell')
     #print(maximum(tritanium_SinqLaison[1],1000), 'maxi buy')
     #sell_tritanium_TheForge_hisec = hiseconly(tritanium_TheForge[0],0.5)
     #buy_tritanium_TheForge_hisec = hiseconly(tritanium_TheForge[1],0.5)
     #print route(10000022, 10000033)
     
     #max_price = maxprice(buy_tritanium_TheForge_hisec)
     print eveid('Tritanium')
     buyercount = 0
     salecount = 9999999999
     '''for x in regionid.keys():
          xorders = queryquicklook('Tritanium', x, 20000)
          sell_xorders_tritanium_highsec = hiseconly(xorders[0],0.5)
          buy_xorders_tritanium_highsec = hiseconly(xorders[1],0.5)
          sale = minprice(sell_xorders_tritanium_highsec)
          buyer = maxprice(buy_xorders_tritanium_highsec)
          if sale !={} and float(sale['price']) < salecount:
               salecount = float(sale['price'])
               sell = sale

          if buyer != {} and float(buyer['price']) > buyercount:
               buyercount = float(buyer['price'])
               buy = buyer
               

     #print sell['price'], sell['station_name']
     #print buy['price'], buy['station_name']

     
     #for reg0 in sell:
          #for reg1 in buy:
               #profit = (float(reg1['price']) - float(reg0['price']) )* float(reg0['vol_remain'])
               #numjump = 
               #f profit >= oldprofit:
                    
     
     import sqlite3 as SQL
     conn = SQL.connect('eve_dump.db')
     conn.text_factory = str
     cur = conn.cursor()
     cur.execute('SELECT System FROM npcstation WHERE StationName=?', (sell['station_name'],))
     sqlthing1 = cur.fetchone()
     cur.execute('SELECT System FROM npcstation WHERE StationName=?', (buy['station_name'],))
     sqlthing2 = cur.fetchone()

     print numberjumpsroute(sqlthing1[0], sqlthing2[0]) , (float(buy['price']) - float(sell['price']))

     conn.close()'''



     
