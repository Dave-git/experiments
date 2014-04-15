import requests as req
from xml.etree import ElementTree as ET

def evecentral(name):
     typeid={'Tritanium':34, 'Thing':35}
     payload = {'typeid':typeid[name]}
     rv = req.get('http://api.eve-central.com/api/marketstat', params=payload)
     return rv.text

def xmlparser(name, response, ordertype):
     dict_resp = {}
     xml = ET.fromstring(response)
     for node in xml.iter(ordertype):
          for subnode in node.iter():
               dict_resp[subnode.tag] = subnode.text
     return dict_resp

if __name__=="__main__":
     

     data = evecentral('Tritanium')
     sell = xmlparser('Tritanium', data,'sell')
     buy = xmlparser('Tritanium', data,'buy')
     print('Sell {0} @ {1} for {2}'.format(sell['volume'], sell['min'], sell['max']))
