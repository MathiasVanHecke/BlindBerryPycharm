from flask import Flask, render_template

import os
app = Flask(__name__)


@app.route('/')
def index():

    return render_template('index.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/log')
def log():
    return render_template('log.html')

@app.route('/automatisatie')
def automatisatie():
    return render_template('automatisatie.html')




@app.errorhandler(404)
def pagenotfound(error):
    return render_template("errors/404.html", error=error)


if __name__ == '__main__':
    port = int(os.environ.get("PORT",5000))
    app.run(host='0.0.0.0',port=5000,debug=True)

