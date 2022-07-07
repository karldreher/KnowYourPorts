import os
from web import create_app
import requests
import os
import ports
import pytest

@pytest.fixture
def app():
    app = create_app()
    return app

@pytest.fixture(scope='session')
def db():

    response = requests.get('https://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.xml')
    with open('service-names-port-numbers.xml', 'wb') as file:
        file.write(response.content)
    ports.setup_db(create_app())
    yield db
    os.remove('service-names-port-numbers.xml')
    os.remove('ports.sqlite')
