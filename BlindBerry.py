from flask import Flask, render_template, url_for, request, redirect, session
from functools import wraps
from DbClass import DbClass
import ctypes
import os
import datetime
import threading

#====Steppermotor===
import RPi.GPIO as GPIO
ControlPin = [7,11,13,15]
# #forlightsensor, temp, steppermotor
#!/usr/bin/python
import spidev
import time
import os

# Open SPI bus
spi = spidev.SpiDev()
spi.open(0, 0)

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
#======Here stops code for sensors & steppermotor============


class Threading(object):
    """ Threading example class
    The run() method will be started and it will run in the background
    until the application exits.
    """

    def __init__(self, interval=10):
        """ Constructor
        :type interval: int
        :param interval: Check interval, in seconds
        """
        self.interval = interval

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True                            # Daemonize thread
        thread.start()                                  # Start the execution


    def run(self):
        """ Method that runs forever """

        while True:
            # Do something

            # Function to read SPI data from MCP3008 chip
            # Channel must be an integer 0-7
            def ReadChannel(channel):
                adc = spi.xfer2([1, (8 + channel) << 4, 0])
                data = ((adc[1] & 3) << 8) + adc[2]
                return data

            # Function to convert data to voltage level,
            # rounded to specified number of decimal places.
            def ConvertVolts(data, places):
                volts = (data * 3.3) / float(1023)
                volts = round(volts, places)
                return volts

            # Function to calculate temperature from
            # TMP36 data, rounded to specified
            # number of decimal places.
            def ConvertTemp(data, places):
                temp = data * 100
                return temp

            # Define sensor channels
            light_channel = 0
            temp_channel = 1

            # Define delay between readings
            delay = 10


            while True:
                # Read the light sensor data
                light_level = ReadChannel(light_channel)
                light_volts = ConvertVolts(light_level, 2)

                # Read the temperature sensor data
                temp_level = ReadChannel(temp_channel)
                temp_volts = ConvertVolts(temp_level, 2)
                temp = ConvertTemp(temp_volts, 2)

                # Print out results

                print("Light: {} ".format(light_level))
                print("Temp : {} deg C".format(int(temp)))
                # licht = light_level
                # temperatuur = temp

                # db = DbClass()
                # db.setDataToData(temperatuur,licht)

                # Wait before repeating loop
                def checkGeenLicht():
                    db = DbClass()
                    print("gecontroleerd op Geen Licht aanstaat")
                    toestandGeenLicht = db.getToestandBlindGeenLicht()
                    if toestandGeenLicht[0] == 1:
                        print("geen licht staat aan.")

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
                            time.sleep(10)
                            print(ldr_value)

                            db = DbClass()
                            toestand = db.getToestandBlind()
                            if ldr_value > 600 and toestand[0] == 1:
                                print("donker")
                                db.updateToestandBlind(0)
                                rolluik_openen("Rolluik omhoog door lichtsensor, omdat het buiten donker is.")

                            elif ldr_value < 600 and toestand[0] == 0:
                                print("licht")
                                db.updateToestandBlind(1)
                                rolluik_sluiten("Rolluik omlaag door lichtsensor, omdat het buiten licht is. ")
                checkGeenLicht()
                def checkWelLicht():
                    db = DbClass()
                    print("gecontroleerd op Licht aanstaat")
                    toestandWelLicht = db.getToestandBlindWelLicht()

                    if toestandWelLicht[0] == 1:
                        print("lichtstaat aan.")

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
                            time.sleep(0.5)
                            db = DbClass()
                            toestand = db.getToestandBlindWelLicht()
                            if ldr_value > 600 and toestand[0] == 1:
                                db.updateToestandBlind(1)
                                rolluik_sluiten("Rolluik omhoog door lichtsensor, omdat het buiten donker is.")

                            elif ldr_value < 600 and toestand[0] == 0:
                                db.updateToestandBlind(0)
                                rolluik_openen("Rolluik omlaag door lichtsensor, omdat het buiten licht is. ")

                checkWelLicht()

                time.sleep(delay)

            time.sleep(self.interval)







app = Flask(__name__)
Threading()


def licht_uit(reden):
    GPIO.setup(40, GPIO.OUT)
    GPIO.output(40, GPIO.LOW)
    datum = datetime.datetime.now()
    uur = datetime.datetime.now()
    reden = reden
    db = DbClass()
    db.setDataToLog(datum, uur, reden)

def licht_aan(reden):
    GPIO.setup(40, GPIO.OUT)
    datum = datetime.datetime.now()
    uur = datetime.datetime.now()
    reden = reden
    db = DbClass()
    db.setDataToLog(datum, uur, reden)
    GPIO.output(40, GPIO.HIGH)

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
    db = DbClass()
    laatste_temp = db.getLaatsteTemperatuur()
    toestandBlind = db.getToestandBlind()
    toestandLicht = db.getToestandLicht()
    if request.method == "POST":
        button = request.form["button"]

        #1 gelosten 0 is open
        print(toestandBlind)
        if button == "open" and toestandBlind[0] == 1:
            db.updateToestandBlind(0)
            rolluik_openen("Rolluik manueel gesloten door de gebruiker.")
            db.updateToestandGeenLicht(0)
            db.updateToestandWelLicht(0)
            return redirect(url_for('home'))

        if button == "sluiten" and toestandBlind[0] == 0:
            db.updateToestandBlind(1)
            rolluik_sluiten("Rolluik manueel geopend door de gebruiker.")
            db.updateToestandGeenLicht(0)
            db.updateToestandWelLicht(0)
            return redirect(url_for('home'))

        if button == "aan" and toestandLicht[0] == 1:
            db.updateToestandLicht(0)
            licht_aan("Licht aan door de gebruiker")
            return redirect(url_for('home'))

        if button == "uit" and toestandLicht[0] == 0:
            db.updateToestandLicht(1)
            licht_uit("Licht uit door de gebruiker")
            return redirect(url_for('home'))



    return render_template('home.html', laatste_temp=laatste_temp[0], toestandBlind=toestandBlind, toestandLicht=toestandLicht)

@app.route('/log', methods=['GET', 'POST'])
@login_nodig

def log():
    db_layer = DbClass()
    lijst_logs = db_layer.getLogs()

    if request.method == "POST":
        button = request.form["button"]
        if button == "verwijder":
            db = DbClass()
            db.deleteDataLog()
    return render_template('log.html', lijst_logs = lijst_logs)



@app.route('/automatisatie', methods=['GET', 'POST'])
@login_nodig
def automatisatie():
    db_layer = DbClass()
    toestandWelLicht = db_layer.getToestandBlindWelLicht()
    toestandGeenLicht = db_layer.getToestandBlindGeenLicht()

    if request.method == "POST":
        button = request.form["button"]
        if button == "geen licht-open gordijn":
            db_layer.updateToestandGeenLicht(1)
            # Define Variables

        if button == "wel licht-open gordijn":
            db_layer.updateToestandWelLicht(1)

        if button == "stop":
            db_layer.updateToestandWelLicht(0)
            db_layer.updateToestandGeenLicht(0)

    return render_template('automatisatie.html', toestandWelLicht = toestandWelLicht, toestandGeenLicht = toestandGeenLicht)




@app.route('/nieuwe_automatisatie', methods=['GET', 'POST'])
@login_nodig
def nieuwe_automatisatie():

    return render_template('nieuwe_automatisatie.html')

@app.route('/grafiek')
@login_nodig
def grafiek():
    db = DbClass()
    lijst = db.getLaatste10Temperaturen()

    return render_template('grafiek.html', lijst=list(reversed(lijst)))

@app.errorhandler(404)
def pagenotfound(error):
    return render_template("errors/404.html", error=error)


if __name__ == '__main__':
    port = int(os.environ.get("PORT",5000))
    app.run(host='0.0.0.0',port=5000,debug=True)