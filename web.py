import ports
import os
from flask_restful import Resource, Api
from flask import Flask, render_template, request, url_for, abort, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
import waitress
PORT = os.environ.get('PORT', 5000)

def create_app():
    #if PORT env is specified, use that, otherwise use port 5000 flask default
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ports.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    ports.db.init_app(app)

    ## API route definitions
    api = Api(app)
    class port(Resource):
        def get(self, num:int):
            result = ports.search_port(num)
            return jsonify(port=num,name=result.name,description=result.description)

    class health(Resource):
        def get(self):
            return jsonify(message='ok')
    api.add_resource(port, '/api/port/<int:num>')
    api.add_resource(health, '/health')


    ## Frontend template route defintions
    @app.route('/index')
    @app.route('/', methods=['GET'])
    def entry():
        return render_template('input_page.html', result=False)

    @app.route('/', methods=['POST'])
    def submit():
        #mysterious, but necessary step.  Without next line, request is null.
        request.get_data()
        userinput = request.form['port_input']
        return redirect(url_for('port_response', num=userinput), 303)

    @app.route('/port/<int:num>', methods=['GET'])
    def port_response(num:int):
        if num == '':
            return render_template('input_page.html', result=False)

        result = ports.search_port(num)

        return render_template('input_page.html', port=num, result=result)

    return app

if __name__ == "__main__":
    app=create_app()
    waitress.serve(app, host='0.0.0.0', port=PORT)
