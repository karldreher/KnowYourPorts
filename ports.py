import xml.etree.ElementTree as ET
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Port(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer)
    name = db.Column(db.String)
    description = db.Column(db.String)
    protocol = db.Column(db.String)


def setup_db(app):
    with app.app_context():
        db.reflect()
        db.drop_all()
        db.create_all()


def update_db(app):
    with app.app_context():
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
    return Port.query.filter_by(number=port_number).first()
