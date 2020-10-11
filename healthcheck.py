import http.client
import os
import logging
from logging.handlers import RotatingFileHandler

PORT = os.environ.get('PORT', 5000)
endpoint = '/healthcheck'

handlerlist = []
handlerlist.append(RotatingFileHandler(filename='healthcheck.log', mode='a', maxBytes=10240, backupCount=1))
logging.basicConfig(handlers=handlerlist, format='%(asctime)s %(levelname)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',level='INFO')

connection = http.client.HTTPConnection('localhost',PORT)

try:
    request = connection.request('GET', endpoint)
    response = connection.getresponse()

    if response.status == 200:
        logging.info('endpoint \"' + endpoint + '\" returned ' + str(response.status) + ' ' + response.reason)

    if response.status >= 400 and response.status < 500:
        logging.error('Healthcheck reported '+ str(response.status) +' against endpoint :\"' + endpoint + '\".  However, this response indicates a web service is running.')
        logging.info('Are you sure this is a KnowYourPorts app?')

    if response.status >= 500 and response.status < 600:
        logging.error('Healthcheck reported '+ str(response.status) +' against endpoint :\"' + endpoint + '\".  More information on next line: ')
        logging.error(response.read())

except:
    logging.fatal('Error, could not request the endpoint \"' + endpoint + '\".  Usually this means a web service is not responding.')

