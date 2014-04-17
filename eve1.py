import requests as req
from xml.etree import ElementTree as ET
thingy = '''<?xml version='1.0' encoding='utf-8'?>
<evec_api version="2.0" method="quicklook">
          <quicklook>
            <item>35</item>
            <itemname>Pyerite</itemname>
            <regions><region>
          Heimatar
        </region></regions>
            <hours>360</hours>
            <minqty>10001</minqty>
            <sell_orders><order id="3522514660">
            <region>10000030</region>
            <station>60015039</station>
            <station_name>Larkugei IX - Republic Military School</station_name>
            <security>0.9</security>
            <range>32767</range>
            <price>12.50</price>
            <vol_remain>2699637</vol_remain>
            <min_volume>1</min_volume>
            <expires>2014-04-23</expires>
            <reported_time>04-16 14:13:54</reported_time>
          </order><order id="3522696799">
            <region>10000030</region>
            <station>60015037</station>
            <station_name>Hadaugago II - Moon 1 - Republic Military School</station_name>
            <security>0.9</security>
            <range>32767</range>
            <price>12.42</price>
            <vol_remain>465718</vol_remain>
            <min_volume>1</min_volume>
            <expires>2014-07-15</expires>
            <reported_time>04-16 14:13:54</reported_time>
          </order><order id="3523653280">
            <region>10000030</region>
            <station>60010294</station>
            <station_name>Osaumuni VII - Moon 16 - CreoDron Factory</station_name>
            <security>0.9</security>
            <range>32767</range>
            <price>12.30</price>
            <vol_remain>959108</vol_remain>
            <min_volume>1</min_volume>
            <expires>2014-04-23</expires>
            <reported_time>04-16 14:13:54</reported_time>
          </order><order id="3524832391">
            <region>10000030</region>
            <station>60006535</station>
            <station_name>Onga VIII - Moon 5 - Imperial Armaments Factory</station_name>
            <security>1.0</security>
            <range>32767</range>
            <price>14.38</price>
            <vol_remain>5455453</vol_remain>
            <min_volume>1</min_volume>
            <expires>2014-04-19</expires>
            <reported_time>04-16 14:13:54</reported_time>
          </order><order id="3410102670">
            <region>10000030</region>
            <station>60006535</station>
            <station_name>Onga VIII - Moon 5 - Imperial Armaments Factory</station_name>
            <security>1.0</security>
            <range>32767</range>
            <price>14.40</price>
            <vol_remain>242253</vol_remain>
            <min_volume>1</min_volume>
            <expires>2014-07-15</expires>
            <reported_time>04-16 14:13:54</reported_time>
          </order><order id="3512719005">
            <region>10000030</region>
            <station>60010297</station>
            <station_name>Onga X - Moon 11 - CreoDron Warehouse</station_name>
            <security>1.0</security>
            <range>32767</range>
            <price>15.00</price>
            <vol_remain>14151</vol_remain>
            <min_volume>1</min_volume>
            <expires>2014-05-16</expires>
            <reported_time>04-16 14:13:54</reported_time>
          </order><order id="3519752147">
            <region>10000030</region>
            <station>60009967</station>
            <station_name>Klir V - Moon 11 - Quafe Company Factory</station_name>
            <security>0.8</security>
            <range>32767</range>
            <price>12.60</price>
            <vol_remain>82253662</vol_remain>
            <min_volume>1</min_volume>
            <expires>2014-04-30</expires>
            <reported_time>04-16 14:13:54</reported_time>
          </order></sell_orders>
            <buy_orders><order id="3460547499">
            <region>10000030</region>
            <station>60015044</station>
            <station_name>Usteli V - Republic University</station_name>
            <security>1.0</security>
            <range>-1</range>
            <price>10.54</price>
            <vol_remain>5000000</vol_remain>
            <min_volume>1</min_volume>
            <expires>2014-07-15</expires>
            <reported_time>04-16 14:13:54</reported_time>
          </order><order id="3428352273">
            <region>10000030</region>
            <station>60015038</station>
            <station_name>Krilmokenur VII - Moon 8 - Republic Military School</station_name>
            <security>0.9</security>
            <range>-1</range>
            <price>11.22</price>
            <vol_remain>117164</vol_remain>
            <min_volume>1</min_volume>
            <expires>2014-07-15</expires>
            <reported_time>04-16 14:13:54</reported_time>
          </order><order id="3483029897">
            <region>10000030</region>
            <station>60004588</station>
            <station_name>Rens VI - Moon 8 - Brutor Tribe Treasury</station_name>
            <security>0.9</security>
            <range>-1</range>
            <price>11.50</price>
            <vol_remain>608785</vol_remain>
            <min_volume>1</min_volume>
            <expires>2014-07-15</expires>
            <reported_time>04-16 14:13:54</reported_time>
          </order></buy_orders>
          </quicklook>
        </evec_api>'''

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
     regionid={'Heimatar':10000030, 'Sinq Laison':10000032}
     payload = {'typeid':typeid[name], 'regionlimit':regionid[region]}
     rv = req.get('http://api.eve-central.com/api/quicklook', params=payload)
     return rv.text

@quicklook
def naughty(thingy):
     return thingy

if __name__=="__main__":
     

     #data = querymarketstat('Tritanium')
     data = queryquicklook('Tritanium', 'Heimatar')
     print type(data[0])
     #print (naughty(thingy))
     #print profit(data['buy']['volume'], data['sell']['min'], data['buy']['max'])
     #sell = xmlparser('Tritanium', data,'sell')
     #buy = xmlparser('Tritanium', data,'buy')
     #print('Sell {0} @ {1} for {2}'.format(sell['volume'], sell['min'], sell['max']))
