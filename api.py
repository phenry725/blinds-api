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

def stopBlindsAfterDelay(duration): #press directional button, then wait and press stop
    sleep(duration)
    pressButton(STOP_GPIO_PIN)

def returnErrorStatus():
    return json.jsonify(
        ok=False
    )

def returnSuccessStatus():
    return json.jsonify(
        ok=True
    )

#define API routes
@app.route("/blinds", methods=['POST'])
def blindControl():
    content = request.get_json()
    if content is None:
        return returnErrorStatus()
    print "Incoming request: " + str(content)
    #Try to set the pin for the command, if not return error
    try
        pin = pinsDict[content['command']]
    except KeyError:
        print "Error invalid or missing command: " + str(content['command'])
        return returnErrorStatus()
    #execute pin press
    pressButton(pin)
    if 'duration' in content:
        stopBlindsAfterDelay(content['duration']) #what if duration is not int, explain difference between press/timed
    return returnSuccessStatus()

# @app.route("/lights", methods=['POST'])
# def lightControl():
#     content = request.get_json()
#
