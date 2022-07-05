import ports
import os
from flask_restful import Resource, Api
from flask import Flask, render_template, request, url_for, abort, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
import waitress
PORT = os.environ.get('PORT', 7000)

def create_app():
    #if PORT env is specified, use that, otherwise use port 5000 flask default
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ports.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    ports.db.init_app(app)
    api = Api(app)

    @app.route('/index')
    @app.route('/', methods=['GET'])
    def entry():
        return render_template('input_page.html', result=False)

    @app.route('/', methods=['POST'])
    def submit():   
        #mysterious, but necessary step.  Without next line, request is null.
        request.get_data()
        userinput = request.form['port_input']
        return redirect(url_for('port_response', submitted_port=userinput), 303)

    @app.route('/port/<int:submitted_port>', methods=['GET'])
    def port_response(submitted_port):

        if submitted_port == '':
            return render_template('input_page.html', result=False)
            
        try:
            portInt = int(submitted_port)
        except ValueError:
            abort(400)

        search_result = ports.search_port(portInt)
        if search_result != None:
            success = True
            result = search_result
        else:
            success = False
            result = "No service found!"

        return render_template('input_page.html', success=success, port=portInt, result=result)


    @app.route ('/healthcheck')
    def healthcheck():
        return 'ok'

    class port(Resource):
        def get(self, num:int):
            result = ports.search_port(num)
            return jsonify(port=num,name=result.name,description=result.description)
    api.add_resource(port, '/api/port/<int:num>')

    return app

if __name__ == "__main__":
    app=create_app()
    waitress.serve(app, host='0.0.0.0', port=PORT)
