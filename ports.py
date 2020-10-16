import xml.etree.ElementTree as ET
import os
import sqlite3
import sys
from collections import namedtuple

sqlite_database = 'ports.sqlite'
sqlite_database_ro = 'file:ports.sqlite?mode=ro'

class empty_text:
    def __init__(self):
        self.text = ""

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
        for port in root.findall('{http://www.iana.org/assignments}record'):
                number = port.find('{http://www.iana.org/assignments}number')
                if number is None:
                    number = empty_text()
                
                name = port.find('{http://www.iana.org/assignments}name')
                if name is None:
                    name = empty_text()
                
                description = port.find('{http://www.iana.org/assignments}description')
                if description is None:
                    description = empty_text()
                

                protocol = port.find('{http://www.iana.org/assignments}protocol')
                if protocol is None:
                    protocol = empty_text()

                cur.execute("INSERT INTO PORTS VALUES (null,?,?,?,?);", (number.text,name.text,description.text,protocol.text))
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

