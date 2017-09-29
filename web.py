import ports
import os
from flask import Flask, render_template, request, url_for

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
    port = request.form['port_input']

    portInt = 0

    try:
        portInt = int(port)
    except:
        return render_template('input_page.html')

    result = ports.search_port(portInt)
    if result != None:      
        explain = "is the port number for"
        success = True
        result = result[1]
    else:
        explain = "No result for "
        result = "No service found!"
        success = False

    return render_template('input_page.html', success=success, port=portInt, result=result, explain=explain)
  
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=PORT)
