import requests as req
from xml.etree import ElementTree as ET

def evecentral(name):
     typeid={'Tritanium':34, 'Thing':35}
     payload = {'typeid':typeid[name]}
     return req.get('http://api.eve-central.com/api/marketstat', params=payload)

def xmlparser(name, responseobject, ordertype):
     buy = {'volume':0,'avg':0,'max':0,'min':0,'stddev':0,'mediam':0,'percentile':0}
     xml = ET.fromstring(response.text)
     for node in xml.iter(ordertype):
          for subnode in node.iter():
               buy[subnode.tag] = subnode.text
     return buy

if __name__=="__main__":
     

     response = evecentral('Tritanium')
     returno = xmlparser('Tritanium', response,'buy')
     print returno

               

     
