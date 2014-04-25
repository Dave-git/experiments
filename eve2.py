import requests as req
from xml.etree import ElementTree as ET

regionid = {'Derelik':10000001,'The Forge':10000002,'Vale of the Silent':10000003,'UUA-F4':10000004,'Detorid':10000005,'Wicked Creek':10000006,'Cache':10000007,'Scalding Pass':10000008,'Insmother':10000009,'Tribute':10000010,'Great Wildlands':10000011,'Curse':10000012,'Malpais':10000013,'Catch':10000014,'Venal':10000015,'Lonetrek':10000016,'J7HZ-F':10000017,'The Spire':10000018,'A821-A':10000019,'Tash-Murkon':10000020,'Outer Passage':10000021,'Stain':10000022,'Pure Blind':10000023,'Immensea':10000025,'Etherium Reach':10000027,'Molden Heath':10000028,'Geminate':10000029,'Heimatar':10000030,'Impass':10000031,'Sinq Laison':10000032,'The Citadel':10000033,'The Kalevala Expanse':10000034,'Deklein':10000035,'Devoid':10000036,'Everyshore':10000037,'The Bleak Lands':10000038,'Esoteria':10000039,'Oasa':10000040,'Syndicate':10000041,'Metropolis':10000042,'Domain':10000043,'Solitude':10000044,'Tenal':10000045,'Fade':10000046,'Providence':10000047,'Placid':10000048,'Khanid':10000049,'Querious':10000050,'Cloud Ring':10000051,'Kador':10000052,'Cobalt Edge':10000053,'Aridia':10000054,'Branch':10000055,'Feythabolis':10000056,'Outer Ring':10000057,'Fountain':10000058,'Paragon Soul':10000059,'Delve':10000060,'Tenerifis':10000061,'Omist':10000062,'Period Basis':10000063,'Essence':10000064,'Kor-Azor':10000065,'Perrigen Falls':10000066,'Genesis':10000067,'Verge Vendor':10000068,'Black Rise':10000069}


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
def queryquicklook(name, region):
     '''requests data from the quicklook endpoint'''
     typeid={'Tritanium':34, 'Pyerite':35}
     payload = {'typeid':typeid[name], 'regionlimit':regionid[region]}
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

def maxprice(orders, volremain):
     '''returns the highest price for orders with a significant volume remaining'''
     max_price = 0
     for x in orders.keys():
          if float(orders[x]['price']) > max_price:
               max_price = orders[x]['price']
               
     return max_price

def minprice(orders, volremain):
     '''returns the highest price for orders with a significant volume remaining'''
     min_price = 9999999999
     for x in orders.keys():
          if float(orders[x]['price']) < min_price:
               min_price = orders[x]['price']
               
     return min_price

if __name__=="__main__":
     
     
     #data = querymarketstat('Tritanium')
     #tritanium_heimatar = queryquicklook('Tritanium', 'Heimatar')
     #tritanium_SinqLaison = queryquicklook('Tritanium', 'Sinq Laison')
     tritanium_TheForge = queryquicklook('Tritanium', 'The Forge')
     #print tritanium_TheForge[0]
     #print(minimum(tritanium_heimatar[0],1000), 'mini sell')
     #print(maximum(tritanium_heimatar[1],1000), 'maxi buy')
     #print(minimum(tritanium_SinqLaison[0],1000), 'mini sell')
     #print(maximum(tritanium_SinqLaison[1],1000), 'maxi buy')
     #sell_tritanium_TheForge_hisec = hiseconly(tritanium_TheForge[0],0.5)
     buy_tritanium_TheForge_hisec = hiseconly(tritanium_TheForge[1],0.5)
     
     max_price = maxprice(buy_tritanium_TheForge_hisec,1000)
     for x in regionid.keys():
          xorders = queryquicklook('Tritanium', x)
          sell_xorders_tritanium_highsec = hiseconly(xorders[0],0.5)
          buy_xorders_tritanium_highsec = hiseconly(xorders[1],0.5)
          #minsell = minprice(sell_xorders_tritanium_highsec, 1000)
          minsell = 2.00
          print(upperlimit(buy_xorders_tritanium_highsec, minsell))
            
          
          #print(upperlimit(sell_xorders_tritanium_highsec, max_price))


     #print(lowerlimit(sell_tritanium_TheForge_hisec,5.35))
     #print(upperlimit(sell_tritanium_TheForge_hisec,3))
     
     #print(maximum(tritanium_TheForge[1],1000), 'maxi buy')         
     #for x in data[0].keys():
          #print data[0][x]['price']
          
     #print (naughty(thingy))
     #print profit(data['buy']['volume'], data['sell']['min'], data['buy']['max'])
     #sell = xmlparser('Tritanium', data,'sell')
     #buy = xmlparser('Tritanium', data,'buy')
