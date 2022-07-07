from flask_restful import Resource, Api
from flask import Flask, render_template, request, url_for, redirect, jsonify
import waitress
import ports


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ports.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    ports.db.init_app(app)

    # API route definitions
    api = Api(app)

    class Port(Resource):
        def get(self, num: int):
            result = ports.search_port(num)
            return jsonify(port=num, name=result.name, description=result.description)

    class Health(Resource):
        def get(self):
            return jsonify(message='ok')

    api.add_resource(Port, '/api/port/<int:num>')
    api.add_resource(Health, '/health')

    # Frontend template route defintions

    @app.route('/index')
    @app.route('/', methods=['GET'])
    def entry():
        return render_template('input_page.html', result=False)

    @app.route('/', methods=['POST'])
    def submit():
        # mysterious, but necessary step.  Without next line, request is null.
        request.get_data()
        userinput = request.form['port_input']
        return redirect(url_for('port_response', num=userinput), 303)

    @app.route('/port/<int:num>', methods=['GET'])
    def port_response(num: int):
        if num == '':
            return render_template('input_page.html', result=False)

        result = ports.search_port(num)

        return render_template('input_page.html', port=num, result=result)

    return app


if __name__ == "__main__":
    flask_app = create_app()
    waitress.serve(flask_app)
