import requests as req
import MySQLdb as SQL
from xml.etree import ElementTree as ET
from HTMLParser import HTMLParser

regionid = {'Derelik':10000001,'The Forge':10000002,'Vale of the Silent':10000003,'UUA-F4':10000004,'Detorid':10000005,'Wicked Creek':10000006,'Cache':10000007,'Scalding Pass':10000008,'Insmother':10000009,'Tribute':10000010,'Great Wildlands':10000011,'Curse':10000012,'Malpais':10000013,'Catch':10000014,'Venal':10000015,'Lonetrek':10000016,'J7HZ-F':10000017,'The Spire':10000018,'A821-A':10000019,'Tash-Murkon':10000020,'Outer Passage':10000021,'Stain':10000022,'Pure Blind':10000023,'Immensea':10000025,'Etherium Reach':10000027,'Molden Heath':10000028,'Geminate':10000029,'Heimatar':10000030,'Impass':10000031,'Sinq Laison':10000032,'The Citadel':10000033,'The Kalevala Expanse':10000034,'Deklein':10000035,'Devoid':10000036,'Everyshore':10000037,'The Bleak Lands':10000038,'Esoteria':10000039,'Oasa':10000040,'Syndicate':10000041,'Metropolis':10000042,'Domain':10000043,'Solitude':10000044,'Tenal':10000045,'Fade':10000046,'Providence':10000047,'Placid':10000048,'Khanid':10000049,'Querious':10000050,'Cloud Ring':10000051,'Kador':10000052,'Cobalt Edge':10000053,'Aridia':10000054,'Branch':10000055,'Feythabolis':10000056,'Outer Ring':10000057,'Fountain':10000058,'Paragon Soul':10000059,'Delve':10000060,'Tenerifis':10000061,'Omist':10000062,'Period Basis':10000063,'Essence':10000064,'Kor-Azor':10000065,'Perrigen Falls':10000066,'Genesis':10000067,'Verge Vendor':10000068,'Black Rise':10000069}






def route(start, finish):
     path = 'http://api.eve-central.com/api/route/from/{0}/to/{1}'.format(start,finish)
     rv = req.get(path)
     return rv.text

def getstations(url):
     rv = req.get(url)
     return rv.text


     

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
     for x in orders.keys():
          if float(orders[x]['price']) < max_price:
               del orders[x]
          else:
               max_price = orders[x]['price']          
               
     return orders

def minprice(orders):
     '''returns the highest price for orders with a significant volume remaining'''
     min_price = 9999999999
     for x in orders.keys():
          if float(orders[x]['price']) > min_price:
               del orders[x]
          else:
               min_price = orders[x]['price']
               
     return orders

class MyHTMLParser(HTMLParser):
     def __init__(self):
          HTMLParser.__init__(self)
          self.intable = False
          self.value = {}
          self.diction = []
          self.righttable = False
          self.a = False
          self.h2 = False
          self.regionname = False
          self.region = ""
          self.working = []
          
     def handle_starttag(self, tag, attrs):
          if tag == 'table':
               self.intable = True
          elif tag == 'h2':
               self.h2 = True
          elif tag == 'a':
               self.a = True
               for x in attrs:
                    #print x
                    if '/region/' in x[1].encode('ascii', 'ignore'):
                         self.regionname = True
                                
     def handle_endtag(self, tag):
          if tag == 'table':
               self.intable = False
               if self.righttable == True:
                    self.righttable = False
          elif tag  == 'tr' and self.righttable == True:
                              
               self.working.append(self.diction)
               #print self.region
               self.value[self.region] = self.working
               self.diction = []
               self.working = []
          
          elif tag == 'h2':
               self.h2 = False
               self.regionname = False
          elif tag == 'a':
               self.regionname = False
               self.a == False
               
               
     def handle_data(self, data):
          if self.h2 == True and self.a == True and self.regionname == True:
               temp = data.encode('ascii', 'ignore')
               #print temp
               self.region = temp
          if 'Constellation' in data and self.intable == True:
               self.righttable = True
          if self.righttable == True:
               temp = data.encode('ascii', 'ignore')
               if not '\n' in temp and temp != ' ':
                    self.diction.append(temp)
     
     def returnvalue(self):
          return self.value
                    
     

if __name__=="__main__":
     
     
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
     #print route(10000056, 10000043)
     
     #max_price = maxprice(buy_tritanium_TheForge_hisec)
     #for x in regionid.keys():
          #xorders = queryquicklook('Pyerite', x, 20000)
          #sell_xorders_tritanium_highsec = hiseconly(xorders[0],0.5)
          #buy_xorders_tritanium_highsec = hiseconly(xorders[1],0.5)
          #print (x, minprice(sell_xorders_tritanium_highsec), maxprice(buy_xorders_tritanium_highsec))
          
          #minsell = minprice(sell_xorders_tritanium_highsec, 1000)
          #minsell = 2.00
     
     amarr1 = ['24th Imperial Crusade', 
              'Amarr Certified News', 
              'Amarr Civil Service', 
              'Amarr Constructions', 
              'Amarr Navy', 
              'Amarr Templars', 
              'Amarr Trade Registry', 
              'Ametat Security', 
              'Ardishapur Family', 
              'Bragian Order', 
              'Carthum Conglomerate', 
              'Civic Court', 
              'Company of Marcher Lords', 
              'Court Chamberlain', 
              'Ducia Foundry', 
              'Emperor Family', 
              'Fraternity of St. Venefice', 
              'Further Foodstuffs', 
              'Hedion University', 
              'Holdfast Syndicate', 
              'HZO Refinery', 
              'Imperial Academy', 
              'Imperial Armaments', 
              'Imperial Chancellor', 
              'Imperial Guard', 
              'Imperial Shipment', 
              'Inherent Implants', 
              'Joint Harvesting', 
              'Kador Family', 
              'Kameira Lodge', 
              'Kor-Azor Family', 
              'Ministry of Assessment', 
              'Ministry of Internal Order', 
              'Ministry of War', 
              'Noble Appliances', 
              'Nurtura', 
              'Paladin Survey Force', 
              'Red and Silver Hand', 
              'Royal Amarr Institute', 
              'Royal Uhlans', 
              'Sarum Family', 
              'Shining Flame', 
              'Tal-Romon Legion', 
              'Tash-Murkon Family', 
              'Theology Council', 
              'Viziam', 
              'Zoar and Sons']
     amarr = ['Zoar and Sons']
     
     for x in amarr:
          url = 'http://evemaps.dotlan.net/npc/{0}/stations'.format(x)
          parser = MyHTMLParser()
          parser.feed(getstations(url))
          moo = parser.returnvalue()
          print moo
          #for i in moo:
               #print  i[0],i[1],i[3]

     
