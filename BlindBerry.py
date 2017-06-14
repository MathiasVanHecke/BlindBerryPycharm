from flask import Flask, render_template, url_for, request, redirect, session
from functools import wraps
from DbClass import DbClass
import ctypes
import os
import datetime

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

def rolluik_openen(reden):
    datum = datetime.datetime.now()
    uur = datetime.datetime.now()
    reden = reden
    db = DbClass()
    db.setDataToLog(datum,uur,reden)

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

def rolluik_sluiten(reden):
    datum = datetime.datetime.now()
    uur = datetime.datetime.now()
    reden = reden
    db = DbClass()
    db.setDataToLog(datum, uur, reden)

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
            rolluik_openen("Rolluik manueel gesloten door de gebruiker.")
        if button == "sluiten":
            rolluik_sluiten("Rolluik manueel geopend door de gebruiker.")
    return render_template('home.html')

@app.route('/log')
@login_nodig
def log():
    db_layer = DbClass()
    lijst_logs = db_layer.getLogs()
    return render_template('log.html', lijst_logs = lijst_logs)


@app.route('/automatisatie', methods=['GET', 'POST'])
@login_nodig
def automatisatie():
    db_layer = DbClass()
    lijst_automatisaties = db_layer.getAutomaisaties()

    switch = 0
    if request.method == "POST":
        button = request.form["button"]
        if button == "geen licht-open gordijn":
            # Define Variables
            delay = 0.5
            ldr_channel = 0

            # Create SPI
            spi = spidev.SpiDev()
            spi.open(0, 0)

            def readadc(adcnum):
                # read SPI data from the MCP3008, 8 channels in total
                if adcnum > 7 or adcnum < 0:
                    return -1
                r = spi.xfer2([1, 8 + adcnum << 4, 0])
                data = ((r[1] & 3) << 8) + r[2]
                return data

            while True:
                ldr_value = readadc(ldr_channel)
                print(ldr_value)
                time.sleep(delay)
                if ldr_value > 600 and switch == 0:
                    switch = 1
                    rolluik_openen("Rolluik omhoog door lichtsensor, omdat het buiten donker is.")

                elif ldr_value < 600 and switch == 1:
                    switch = 0
                    rolluik_sluiten("Rolluik omlaag door lichtsensor, omdat het buiten licht is. ")


    return render_template('automatisatie.html')



@app.route('/nieuwe_automatisatie', methods=['GET', 'POST'])
@login_nodig
def nieuwe_automatisatie():

    return render_template('nieuwe_automatisatie.html')

@app.errorhandler(404)
def pagenotfound(error):
    return render_template("errors/404.html", error=error)


if __name__ == '__main__':
    port = int(os.environ.get("PORT",5000))
    app.run(host='0.0.0.0',port=5000,debug=True)

