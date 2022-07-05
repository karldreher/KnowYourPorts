from flask import Flask, jsonify, request
from flask_restful import Resource, Api
import ports
import os
import waitress

PORT = os.environ.get('PORT', 5000)



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ports.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
ports.db.init_app(app)
api = Api(app)

class port(Resource):
    def get(self, num:int):
        result = ports.search_port(num)
        return jsonify(port=num,name=result.name,description=result.description)


api.add_resource(port, '/port/<int:num>')

if __name__ == '__main__':
    waitress.serve(app, host='0.0.0.0', port=PORT)
