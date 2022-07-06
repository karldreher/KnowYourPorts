import xml.etree.ElementTree as ET
import os
from flask_sqlalchemy import SQLAlchemy
from flask import Flask


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ports.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Port(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer)
    name = db.Column(db.String)
    description = db.Column(db.String)
    protocol = db.Column(db.String)


def setup_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()

        tree = ET.parse('service-names-port-numbers.xml')
        root = tree.getroot()
        keys = {'number', 'name', 'description', 'protocol'}

        for record in root.findall('{*}record'):
            portData = dict.fromkeys(keys)
            for key in keys:
                # ensure all keys are filled with some data.
                portData[key] = ''

            for port in record:
                for key in keys:
                    # if namespace is present (which it will be), remove it
                    tag = port.tag.replace('{http://www.iana.org/assignments}', '')
                    if tag != key:
                        pass
                    else:
                        if port.text is None:
                            pass
                        else:
                            text = port.text
                        portData[key] = text
            port = Port(number=portData['number'], name=portData['name'], description=portData['description'],
                        protocol=portData['protocol'])
            db.session.add(port)
        db.session.commit()


def search_port(number):
    port_number = str(number)
    return Port.query.filter_by(number=port_number).first_or_404()

if __name__ == "__main__":
    if (os.path.exists("ports.sqlite") == False):
        setup_db(app)
