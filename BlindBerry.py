from flask import Flask, render_template, url_for, request, redirect, session
from functools import wraps
from DbClass import DbClass
import ctypes
import os

#====Stepper and light sensor===

import RPi.GPIO as GPIO
import time
#forlightsensor
import spidev

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

ControlPin = [7,11,13,15]

#=================

app = Flask(__name__)

app.secret_key = "my precious"

#login nodig
def login_nodig(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('login'))
    return wrap


@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == "POST":
        db = DbClass()
        user_credentials = db.getUsername(request.form['username'])
        if user_credentials:  # Als de lijst NIET leeg is dan...
            if (user_credentials[1]) != request.form['password']:
                error = "Wachtwoord is onjuist!"
            else:
                session['logged_in'] = True
                session['username'] = user_credentials[0]
                return redirect(url_for("home"))
        else:
            error = "De opgegeven combinatie bestaat niet!"

    return render_template('index.html', error= error)

@app.route('/registreer', methods=['GET', 'POST'])
def registreer():
    return render_template('registreer.html')


@app.route('/logout', methods=['GET', 'POST'])
@login_nodig
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))


@app.route('/home', methods=['GET', 'POST'])
@login_nodig
def home():
    if request.method == "POST":
        button = request.form["button"]
        if button == "open":
            for pin in ControlPin:
                GPIO.setup(pin, GPIO.OUT)
                GPIO.output(pin, 0)

            seq = [[1, 0, 0, 0],
                   [1, 1, 0, 0],
                   [0, 1, 0, 0],
                   [0, 1, 1, 0],
                   [0, 0, 1, 0],
                   [0, 0, 1, 1],
                   [0, 0, 0, 1],
                   [1, 0, 0, 1]]

            for i in range(512):
                ### GO THROUGH THE SEQUENCE ONCE ###
                for halfstep in range(8):
                    ### GO THROUGH EACH HALF-STEP ###
                    for pin in range(4):
                        ### SET EACH PIN ###
                        GPIO.output(ControlPin[pin], seq[halfstep][pin])
                    time.sleep(0.001)
        if button == "sluiten":
            for pin in ControlPin:
                GPIO.setup(pin, GPIO.OUT)
                GPIO.output(pin, 0)

            seq = [[0, 0, 0, 1],
                   [0, 0, 1, 1],
                   [0, 0, 1, 0],
                   [0, 1, 1, 0],
                   [0, 1, 0, 0],
                   [1, 1, 0, 0],
                   [1, 0, 0, 0],
                   [1, 0, 0, 1]]

            for i in range(512):
                ### GO THROUGH THE SEQUENCE ONCE ###
                for halfstep in range(8):
                    ### GO THROUGH EACH HALF-STEP ###
                    for pin in range(4):
                        ### SET EACH PIN ###
                        GPIO.output(ControlPin[pin], seq[halfstep][pin])
                    time.sleep(0.001)
    return render_template('home.html')

@app.route('/log')
@login_nodig
def log():
    db_layer = DbClass()
    lijst_logs = db_layer.getLogs()
    return render_template('log.html', lijst_logs = lijst_logs)


@app.route('/automatisatie')
@login_nodig
def automatisatie():
    db_layer = DbClass()
    lijst_automatisaties = db_layer.getAutomaisaties()

    return render_template('automatisatie.html', lijst_automatisaties = lijst_automatisaties)



@app.route('/nieuwe_automatisatie', methods=['GET', 'POST'])
@login_nodig
def nieuwe_automatisatie():
    if request.method == "POST":
        db = DbClass()
        naam = request.form['naam']
        uurStart = request.form['uurStart']
        uurStop = request.form['uurstop']
        beschrijving= ""
        db.setDataToAutomatisatie(naam,uurStart,uurStop,beschrijving)


    return render_template('nieuwe_automatisatie.html')

@app.errorhandler(404)
def pagenotfound(error):
    return render_template("errors/404.html", error=error)


if __name__ == '__main__':
    port = int(os.environ.get("PORT",5000))
    app.run(host='0.0.0.0',port=5000,debug=True)

