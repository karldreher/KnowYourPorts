import ports
from flask import Flask, render_template, request, url_for


app = Flask(__name__)

@app.route('/index')
@app.route('/', methods=['GET'])
def entry():
    return render_template('input_page.html')


@app.route('/', methods=['POST'])
def submit():
    #mysterious, but necessary step.  Without next line, request is null.
    #Alternative is to hard-code request MIME type, which is the "good" way...
    request.get_data()
    port = request.form['port_input']
    explain = "is the port number for"
    result = ports.search_port(port)
    return render_template('input_page.html', port=port, result=result[1], explain=explain)
    
if __name__ == "__main__":
    app.run()
