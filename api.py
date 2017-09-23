#load API frameworks
# from flask import Flask
# app = Flask(__name__)

#load GPIO framework and set correct pin layout
try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Error importing RPi.GPIO!  This is probably because you need superuser privileges.  You can achieve this by using 'sudo' to run your script")

from time import sleep

UP_GPIO_PIN = 3
STOP_GPIO_PIN = 5
DOWN_GPIO_PIN = 7

#configure channels for blind control
#def initPins():
    #turns out when you initialize the
    #GPIO pin (high or low) it "presses" the button

#cleanup pins
def resetPins():
    GPIO.cleanup()


#define button presses
def pressButton(pin):
    if GPIO.getmode() != GPIO.BOARD:   #set the board mode at time of press if not set
        GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pin, GPIO.OUT, initial=0)  #power the pin then remove the power
    sleep(0.5)
    GPIO.cleanup(pin)

def timedBlindMotion(pin, duration): #press directional button, then wait and press stop
    pressButton(pin)
    time.sleep(duration)
    pressButton(STOP_GPIO_PIN)

#define API routes
# @app.route("/blinds", methods=['POST'])
# def blindControl():
    # client_id = request.args.get('client_id', '')
    # client_secret = request.args.get('client_secret', '')
