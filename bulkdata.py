import requests as req
from xml.etree import ElementTree as ET
from HTMLParser import HTMLParser
import sqlite3 as SQL
import io


def getstations(url):
     rv = req.get(url)
     return rv.text

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
                    self.value[self.region] = self.working
                    self.working = []
                    self.righttable = False
          elif tag  == 'tr' and self.righttable == True and self.diction != []:
                              
               self.working.append(self.diction)
               self.diction = []
          
          elif tag == 'h2':
               self.h2 = False
               self.regionname = False
          elif tag == 'a':
               self.regionname = False
               self.a == False
               
               
     def handle_data(self, data):
          if self.h2 == True and self.a == True and self.regionname == True:
               self.region = data.encode('ascii', 'ignore')
          if 'Constellation' in data and self.intable == True:
               self.righttable = True
          if self.righttable == True:
               temp = data.encode('ascii', 'ignore')
               if not '\n' in temp and temp != ' ':
                    if (temp not in ('Constellation', 'System', 'Security', 'Name', 'Type')):
                         self.diction.append(temp)
     
     def returnvalue(self):
          return self.value
                    
     

if __name__=="__main__":
     systems = []
     npc_stations= ['24th Imperial Crusade', 
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
              'Zoar and Sons', 'Ammatar Consulate',
              'Ammatar Fleet',
              'Nefantar Miner Association',
              'Archangels',
              'Dominations',
              'Guardian Angels',
              'Salvation Angels',
              'Blood Raiders',
              'Caldari Business Tribunal',
              'Caldari Constructions',
              'Caldari Funds Unlimited',
              'Caldari Navy',
              'Caldari Provisions',
              'Caldari Steel',
              'CBD Corporation',
              'CBD Sell Division',
              'Chief Executive Panel',
              'Commando Perkone',
              'Corporate Police Force',
              'Deep Core Mining Inc.',
              'Echelon Entertainment',
              'Expert Distribution',
              'Expert Housing',
              'Expert Intervention',
              'Home Guard',
              'House of Records',
              'Hyasyoda Corporation',
              'Ikomari-Onu Enforcement',
              'Intara Direct Action',
              'Internal Security',
              'Ishukone Corporation',
              'Ishukone Watch',
              'Isuuaya Tactical',
              'Kaalakiota Corporation',
              'Kinsho Swords',
              'Kirkinen Risk Control',
              'Lai Dai Corporation',
              'Lai Dai Protection Service',
              'Mercantile Club',
              'Minedrill',
              'Modern Finances',
              'Nugoeihuvi Corporation',
              'Onikanabo Brigade',
              'Osmon Surveillance',
              'Peace and Order Unit',
              'Perkone',
              'Poksu Mineral Group',
              'Prompt Delivery',
              'Propel Dynamics',
              'Rapid Assembly',
              'School of Applied Knowledge',
              'Science and Trade Institute',
              'Seituoda Taskforce Command',
              'Spacelane Patrol',
              'State and Region Bank',
              'State Peacekeepers',
              'State Protectorate',
              'State War Academy',
              'Storm Wind Strikeforce',
              'Sukuuvestaa Corporation',
              'Templis Dragonaurs',
              'Top Down',
              'Wiyrkomi Corporation',
              'Wiyrkomi Peace Corps',
              'Ytiri',
              'Zainou',
              'Zero-G Research Firm',
              'Zumari Force Projection',
              'CONCORD',
              'DED',
              'Inner Circle',
              'Secure Commerce Commission',
              'Algintal Core',
              'Aliastra',
              'Allotek Industries',
              'Astral Mining Inc.',
              'Bank of Luminaire',
              'Center for Advanced Studies',
              'Chatelain Rapid Response',
              'Chemal Tech',
              'Combined Harvest',
              'Condotta Rouvenor',
              'CreoDron',
              'Crux Special Tasks Group',
              'Duvolle Laboratories',
              'Edimmu Warfighters',
              'Egonics Inc.',
              'Federal Administration',
              'Federal Defense Union',
              'Federal Freight',
              'Federal Intelligence Office',
              'Federal Marines',
              'Federal Navy Academy',
              'Federation Customs',
              'Federation Navy',
              'FedMart',
              'Garoun Investment Bank',
              'Impetus',
              'Inner Zone Shipping',
              'Kang Lo Directorate',
              'Mannar Focused Warfare',
              'Material Acquisition',
              'Namtar Elite',
              'Ostrakon Agency',
              'Pend Insurance',
              'Poteque Pharmaceuticals',
              'President',
              'Quafe Company',
              'Resheph Interstellar Strategy',
              'Roden Shipyards',
              'Senate',
              'Sinq Laison Gendarmes',
              'Supreme Court',
              'The Scope',
              'TransStellar Shipping',
              'University of Caille',
              'Villore Sec Ops',
              'Guristas',
              'Guristas Production',
              'Academy of Aggressive Behaviour',
              'Genolution',
              'Impro',
              'Jove Navy',
              'Jovian Directorate',
              'Material Institute',
              'Prosper',
              'Shapeset',
              'X-Sense',
              'Khanid Innovation',
              'Khanid Transport',
              'Khanid Works',
              'Royal Khanid Navy',
              'Boundless Creation',
              'Brutor Tribe',
              'Brutor Vanguard',
              'Circle of Huskarl',
              'Core Complexion Inc.',
              'Eifyr and Co.',
              'Eyniletti Rangers',
              'Forty-Nine Fedayeen',
              'Freedom Extension',
              'Krullefor Organization',
              'Krusual Covert Operators',
              'Krusual Tribe',
              'Mikramurka Shock Troop',
              'Minmatar Mining Corporation',
              'Native Freshfood',
              'Pator Tech School',
              'Republic Command',
              'Republic Fleet',
              'Republic Justice Department',
              'Republic Military School',
              'Republic Parliament',
              'Republic Security Services',
              'Republic University',
              'Sanmatar Kelkoons',
              'Sebiestor Field Sappers',
              'Sebiestor Tribe',
              'Seykal Expeditionary Group',
              'Six Kin Development',
              'The Leisure Group',
              'Tribal Liberation Force',
              'Tronhadar Free Guard',
              'Urban Management',
              'Vherokior Combat Logistics',
              'Vherokior Tribe',
              'Outer Ring Excavations',
              'True Creations',
              'True Power',
              'Serpentis Corporation',
              'Serpentis Inquest',
              'Food Relief',
              'Sisters of EVE',
              'The Sanctuary',
              'InterBus',
              'Society of Conscious Thought',
              'Intaki Bank',
              'Intaki Commerce',
              'Intaki Space Police',
              'Intaki Syndicate',
              'Thukker Mix',
              'Trust Partners',
              'Arkombine']
     

     tup = ()
     regionid = {'Derelik':10000001,'The Forge':10000002,'Vale of the Silent':10000003,'UUA-F4':10000004,'Detorid':10000005,'Wicked Creek':10000006,'Cache':10000007,'Scalding Pass':10000008,'Insmother':10000009,'Tribute':10000010,'Great Wildlands':10000011,'Curse':10000012,'Malpais':10000013,'Catch':10000014,'Venal':10000015,'Lonetrek':10000016,'J7HZ-F':10000017,'The Spire':10000018,'A821-A':10000019,'Tash-Murkon':10000020,'Outer Passage':10000021,'Stain':10000022,'Pure Blind':10000023,'Immensea':10000025,'Etherium Reach':10000027,'Molden Heath':10000028,'Geminate':10000029,'Heimatar':10000030,'Impass':10000031,'Sinq Laison':10000032,'The Citadel':10000033,'The Kalevala Expanse':10000034,'Deklein':10000035,'Devoid':10000036,'Everyshore':10000037,'The Bleak Lands':10000038,'Esoteria':10000039,'Oasa':10000040,'Syndicate':10000041,'Metropolis':10000042,'Domain':10000043,'Solitude':10000044,'Tenal':10000045,'Fade':10000046,'Providence':10000047,'Placid':10000048,'Khanid':10000049,'Querious':10000050,'Cloud Ring':10000051,'Kador':10000052,'Cobalt Edge':10000053,'Aridia':10000054,'Branch':10000055,'Feythabolis':10000056,'Outer Ring':10000057,'Fountain':10000058,'Paragon Soul':10000059,'Delve':10000060,'Tenerifis':10000061,'Omist':10000062,'Period Basis':10000063,'Essence':10000064,'Kor-Azor':10000065,'Perrigen Falls':10000066,'Genesis':10000067,'Verge Vendor':10000068,'Black Rise':10000069}
     
     #for corporation in npc_stations:
          #url = 'http://evemaps.dotlan.net/npc/{0}/stations'.format(corporation)
          #parser = MyHTMLParser()
          #parser.feed(getstations(url))
          #moo = parser.returnvalue()
          #for y in moo.keys():
               #for z in moo[y]:
                    #tup += (y,)
                    #for q in z:
                         #tup += (q,)
                    #print tup
                    #systems.append(tup)
                    #tup = ()     
     #rows = []
     conn = SQL.connect('eve_dump.db')
     conn.text_factory = str
     cur = conn.cursor()
     #for x in regionid.keys():
          #rows.append((x, regionid[x]))
     
     #print rows
     #cur.execute('''CREATE TABLE typeid (TypeID, Type)''')
     #conn.commit()
     #cur.executemany('INSERT INTO npcstation VALUES (?,?,?,?,?,?)',systems)
     #conn.commit() 
     moop = cur.execute('SELECT * FROM typeid WHERE type ="Kernite"')
     print moop.fetchall()
     row = ()
     #with io.open('C:\\Users\\davidr\\Downloads\\typeid.txt', 'rb') as file:
          #lines = file.readlines()
          #for line in lines:
               #moo= line.replace('\r\n', '', 1).split(',',2)
               #moo =  line.split(",",2)
               #print moo[1]
               #row = (moo[0], moo[1])
               #cur.execute('INSERT INTO typeid VALUES (?,?)', row)
               #conn.commit()               
               #row = ()

     #cur.execute('''CREATE TABLE regionid (RegionName, RegionId)''')
     #conn.commit() 

     
          


     conn.close()
     