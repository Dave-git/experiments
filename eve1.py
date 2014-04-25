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


def minimum(orders, threshold):
     highsec_mini = 9999999999999.00
     lowsec_mini = 9999999999999.00
     highsec_orderid = 0
     lowsec_orderid = 0
     for x in orders.keys():
          if float(orders[x]['price']) <= highsec_mini and orders[x]['vol_remain'] >= threshold and float(orders[x]['security']) >= 0.5:
               hisec_mini = float(orders[x]['price'])
               highsec_orderid = x
          elif float(orders[x]['price']) <= lowsec_mini and orders[x]['vol_remain'] >= threshold:
               lowsec_mini = float(orders[x]['price'])
               lowsec_orderid = x               
          
               
     return orders[highsec_orderid]

def maximum(orders, threshold):
     highsec_max = 0
     lowsec_max = 0
     highsec_orderid = 0
     lowsec_orderid = 0
     for x in orders.keys():
          if float(orders[x]['price']) >= highsec_max and orders[x]['vol_remain'] >= threshold and float(orders[x]['security']) >= 0.5:
               hisec_max = float(orders[x]['price'])
               highsec_orderid = x
          elif float(orders[x]['price']) >= lowsec_max and orders[x]['vol_remain'] >= threshold:
               lowsec_max = float(orders[x]['price'])
               lowsec_orderid = x               
          
               
     return orders[highsec_orderid]

if __name__=="__main__":
     
     
     #data = querymarketstat('Tritanium')
     #tritanium_heimatar = queryquicklook('Tritanium', 'Heimatar')
     #tritanium_SinqLaison = queryquicklook('Tritanium', 'Sinq Laison')
     tritanium_TheForge = queryquicklook('Tritanium', 'The Forge')
     print tritanium_TheForge[0]
     #print(minimum(tritanium_heimatar[0],1000), 'mini sell')
     #print(maximum(tritanium_heimatar[1],1000), 'maxi buy')
     #print(minimum(tritanium_SinqLaison[0],1000), 'mini sell')
     #print(maximum(tritanium_SinqLaison[1],1000), 'maxi buy')
     print(minimum(tritanium_TheForge[0],1000))
     #print(maximum(tritanium_TheForge[1],1000), 'maxi buy')         
     #for x in data[0].keys():
          #print data[0][x]['price']
          
     #print (naughty(thingy))
     #print profit(data['buy']['volume'], data['sell']['min'], data['buy']['max'])
     #sell = xmlparser('Tritanium', data,'sell')
     #buy = xmlparser('Tritanium', data,'buy')
     #print('Sell {0} @ {1} for {2}'.format(sell['volume'], sell['min'], sell['max']))
