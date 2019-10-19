import ports
import os
from flask import Flask, render_template, request, url_for
import waitress

PORT = os.environ.get('PORT', 80)
app = Flask(__name__)

@app.route('/index')
@app.route('/', methods=['GET'])
def entry():
    return render_template('input_page.html', result=False)

@app.route('/', methods=['POST'])
def submit():
    #mysterious, but necessary step.  Without next line, request is null.
    #Alternative is to hard-code request MIME type, which is the "good" way...
    request.get_data()
    submitted_port = request.form['port_input']

    try:
        portInt = int(submitted_port)
    except:
        return render_template('input_page.html')

    result = ports.search_port(portInt)
    if result != None:      
        success = True
        result = result[1]
    else:
        success = False
        result = "No service found!"

    return render_template('input_page.html', success=success, port=portInt, result=result)

if __name__ == "__main__":
    ports.setup_db()
    ports.update_db()
    waitress.serve(app, host='0.0.0.0', port=PORT)
