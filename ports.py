import xml.etree.ElementTree as ET
import os
import sqlite3
import sys


def setup_db():
    #needs to be run manually.  If you downloaded this and it came with the SQLITE file, no need unless you want to set up from scratch.  
    db = None
    db_exist = os.path.isfile('ports.sqlite')
    if db_exist == True:
        os.remove('ports.sqlite')
    else:
        pass
    #connect to db and create table for ports.  
    db = sqlite3.connect('ports.sqlite')
    cur = db.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS PORTS(Record INTEGER PRIMARY KEY AUTOINCREMENT, Port TEXT, Description TEXT, Protocol TEXT)")
    db.commit()
    db.close()

def listports():
    #function mainly for testing purposes, to gauge the quality of the data.
        tree = ET.parse('service-names-port-numbers.xml')
        root = tree.getroot()
        for port in root.findall('{http://www.iana.org/assignments}record'):
                number = port.find('{http://www.iana.org/assignments}number')
                name = port.find('{http://www.iana.org/assignments}description')
                protocol = port.find('{http://www.iana.org/assignments}protocol')
                if number != None:
                    if protocol != None:
                        print(number.text,name.text,protocol.text)

def update_db():
    #not perfect.  Needs duplicate removal.  Some records are listed twice.
    #needs to be run manually after first setup.  
        tree = ET.parse('service-names-port-numbers.xml')
        root = tree.getroot()

        db = sqlite3.connect('ports.sqlite')
        cur = db.cursor()
        for port in root.findall('{http://www.iana.org/assignments}record'):
                number = port.find('{http://www.iana.org/assignments}number')
                name = port.find('{http://www.iana.org/assignments}description')
                protocol = port.find('{http://www.iana.org/assignments}protocol')
                if number != None:
                    if protocol != None:
                        cur.execute("INSERT INTO PORTS VALUES (null,?,?,?);", (number.text,name.text,protocol.text))
        db.commit()
        db.close()

def search_port(number):
        query = str(number)
        db = sqlite3.connect('ports.sqlite')
        cur = db.cursor()
        cur.execute("SELECT Port,Description,upper(Protocol) FROM PORTS WHERE Port=?", (query,))
        db.commit()

        #for now, fetchone to get single entry.
        #some items are duped in the DB, when "instant search" can be implemented in web,
        #clean up the dupes and change this to fetchall.
        row = cur.fetchone()
        db.close()
        
        if row != None:
            #when transport protocol features can be implemented, edit this to include str(row[2])
                return str(row[0]), str(row[1])
        else:
                return None

