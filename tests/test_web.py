from flask import url_for
import requests

def test_entry(client):
    assert client.get(url_for('entry')).status_code == 200

def test_healthcheck(client):
    assert client.get(url_for('healthcheck')).status_code == 200

def test_port_response(client,db):
    assert client.get(url_for('port_response', submitted_port=23)).status_code == 200
