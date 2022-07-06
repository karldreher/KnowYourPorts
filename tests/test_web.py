from flask import url_for
import requests

def test_entry(client):
    assert client.get(url_for('entry')).status_code == 200

def test_healthcheck(client):
    assert client.get(url_for('healthcheck')).status_code == 200

def test_port_response(client,db):
    assert client.get(url_for('port_response', submitted_port=23)).status_code == 200
    assert client.get(url_for('port_response', submitted_port=1111111111)).status_code == 404

def test_api(client,db):
    #Good result, expect 200
    assert client.get(url_for('port', num=53)).status_code == 200
    # Test response data
    data = client.get(url_for('port', num=53)).json
    assert data['description']=='Domain Name Server'
    assert data['name']=='domain'
    assert data['port']==53

    # Bad result, expect 404
    assert client.get(url_for('port', num=400000)).status_code == 404
