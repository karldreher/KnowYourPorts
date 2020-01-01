import xml.etree.ElementTree as ET
import os
import sqlite3
import sys

class empty_text:
    def __init__(self):
        self.text = ""


def setup_db():
    db = None
    db_exist = os.path.isfile('ports.sqlite')
    if db_exist == True:
        os.remove('ports.sqlite')
    else:
        pass
    #connect to db and create table for ports.  
    db = sqlite3.connect('ports.sqlite')
    cur = db.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS PORTS(Record INTEGER PRIMARY KEY AUTOINCREMENT, Port TEXT, Name TEXT, Description TEXT, Protocol TEXT)")
    db.commit()
    db.close()

def listports():
    #function mainly for testing purposes, to gauge the quality of the data.
        tree = ET.parse('service-names-port-numbers.xml')
        root = tree.getroot()
        for port in root.findall('{http://www.iana.org/assignments}record'):
                number = port.find('{http://www.iana.org/assignments}number')
                if number == None:
                    number = empty_text()
                
                name = port.find('{http://www.iana.org/assignments}name')
                if name == None:
                    name = empty_text()
                
                description = port.find('{http://www.iana.org/assignments}description')
                if description == None:
                    description = empty_text()
                

                protocol = port.find('{http://www.iana.org/assignments}protocol')
                if protocol == None:
                    protocol = empty_text()
                
                print(number.text,name.text,description.text,protocol.text)

def update_db():
        tree = ET.parse('service-names-port-numbers.xml')
        root = tree.getroot()

        db = sqlite3.connect('ports.sqlite')
        cur = db.cursor()
        for port in root.findall('{http://www.iana.org/assignments}record'):
                number = port.find('{http://www.iana.org/assignments}number')
                if number == None:
                    number = empty_text()
                
                name = port.find('{http://www.iana.org/assignments}name')
                if name == None:
                    name = empty_text()
                
                description = port.find('{http://www.iana.org/assignments}description')
                if description == None:
                    description = empty_text()
                

                protocol = port.find('{http://www.iana.org/assignments}protocol')
                if protocol == None:
                    protocol = empty_text()
                cur.execute("INSERT INTO PORTS VALUES (null,?,?,?,?);", (number.text,name.text,description.text,protocol.text))
        db.commit()
        db.close()

def search_port(number):
        query = str(number)
        db = sqlite3.connect('ports.sqlite')
        cur = db.cursor()
        cur.execute("SELECT Port,Name,Description,upper(Protocol) FROM PORTS WHERE Port=?", (query,))
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

