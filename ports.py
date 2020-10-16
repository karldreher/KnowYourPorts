import xml.etree.ElementTree as ET
import os
import sqlite3
import sys
from collections import namedtuple

sqlite_database = 'ports.sqlite'
sqlite_database_ro = 'file:ports.sqlite?mode=ro'

labels = ['number','name','description','protocol']

def setup_db():
    db = None
    db_exist = os.path.isfile(sqlite_database)
    if db_exist == True:
        os.remove(sqlite_database)
    else:
        pass
    #connect to db and create table for ports.  
    db = sqlite3.connect(sqlite_database)
    cur = db.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS PORTS(Record INTEGER PRIMARY KEY AUTOINCREMENT, Port TEXT, Name TEXT, Description TEXT, Protocol TEXT)")
    db.commit()
    db.close()

def update_db():
        tree = ET.parse('service-names-port-numbers.xml')
        root = tree.getroot()

        db = sqlite3.connect(sqlite_database)
        cur = db.cursor()
        keys = {'number','name','description','protocol'}
        for record in root.findall('{*}record'):
            portData = dict.fromkeys(keys)
            for port in record:
                for key in keys:
                    #if namespace is present (which it will be), remove it
                    tag = port.tag.replace('{http://www.iana.org/assignments}','')
                    if tag != key:
                        pass
                    else:
                        #if text is None, replace with empty string
                        if port.text is None:
                            text = ''
                        else:
                            text = port.text
                        portData[key] = text
                        #final data quality check, if these keys do not exist create them, fill with empty string.
                        if portData.get(key, -1) != -1:
                            pass
                        else:
                            portData[key] = ''


            cur.execute("INSERT INTO PORTS VALUES (null,?,?,?,?);", (portData['number'],portData['name'],portData['description'],portData['protocol']))
            db.commit()
        db.close()

def search_port(number):
        query = str(number)
        db = sqlite3.connect(sqlite_database_ro, uri=True)
        cur = db.cursor()
        cur.execute("SELECT Port,Name,Description,upper(Protocol) FROM PORTS WHERE Port=?", (query,))
        db.commit()

        #for now, fetchone to get single entry.
        #some items are duped in the DB, when "instant search" can be implemented in web,
        #clean up the dupes and change this to fetchall.
        row = cur.fetchone()
        db.close()
        
        if row != None:
            result = namedtuple("Port", labels)(*row)
            return result
        

        else:
            return None

