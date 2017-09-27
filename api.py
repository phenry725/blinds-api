#load API frameworks
from time import sleep
import RPi.GPIO as GPIO
from flask import Flask, request, json
app = Flask(__name__)

UP_GPIO_PIN = 37
STOP_GPIO_PIN = 35
DOWN_GPIO_PIN = 33

pinsDict = {}
pinsDict['up'] = UP_GPIO_PIN
pinsDict['down'] = DOWN_GPIO_PIN
pinsDict['stop'] = STOP_GPIO_PIN

#configure channels for blind control
def initPins():
    if GPIO.getmode() != GPIO.BOARD:   #set the board mode at time of press if not set
        GPIO.setmode(GPIO.BOARD)

#cleanup pins
def resetPins():
    GPIO.cleanup()

#define button presses
def pressButton(pin):
    if GPIO.getmode() !=  GPIO.BOARD:
        initPins()
    GPIO.setup(pin, GPIO.OUT, initial=0)  #power the pin then remove the power
    sleep(0.5)
    GPIO.cleanup(pin)

def timedBlindMotion(pin, duration): #press directional button, then wait and press stop
    pressButton(pin)
    sleep(duration)
    pressButton(STOP_GPIO_PIN)

#define API routes
@app.route("/blinds", methods=['POST'])
def blindControl():
    print request
    content = request.get_json()
    print "Incoming request: " + str(content)
    if content is None:
        return json.jsonify(
            ok=False
        )
    try:
        pin = pinsDict[content['command']]
        if 'duration' in content:
            timedBlindMotion(pin, content['duration'])
        else:
            pressButton(pin)
    except KeyError:
        print "Error invalid command: " + str(content['command'])
        return json.jsonify(
            ok=False
        )
    return json.jsonify(
        ok=True
    )
