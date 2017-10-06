#load API frameworks
from time import sleep
import RPi.GPIO as GPIO
from flask import Flask, request, json
app = Flask(__name__)

#Pin numbers based on Board mapping for Raspbery Pi 3 Model B
UP_GPIO_PIN = 37
STOP_GPIO_PIN = 35
DOWN_GPIO_PIN = 33

#multi-step because it doesn't look like python supports simultaneous instansiation and load
pinsDict = {}
pinsDict['up'] = UP_GPIO_PIN
pinsDict['down'] = DOWN_GPIO_PIN
pinsDict['stop'] = STOP_GPIO_PIN

##############
#GPIO CONTROL#
##############
#configure board for correct pin mapping
def initPins():
    if GPIO.getmode() != GPIO.BOARD:   #set the board mode at time of press if not set
        GPIO.setmode(GPIO.BOARD)

#cleanup pins
def resetPins():
    GPIO.cleanup()

#on remote, single press will cause steppers to progress to the limit in that direction
def pressButton(pin):
    if GPIO.getmode() !=  GPIO.BOARD:
        initPins()
    GPIO.setup(pin, GPIO.OUT, initial=0)  #setting up the pin causes the button to "press" on the remote
    sleep(0.5)                            #add delay so the motors have time to get the command
    GPIO.cleanup(pin)

#add a delay then stop, used for timed motion i.e. "go up for 3 seconds"
def stopBlindsAfterDelay(duration):
    sleep(duration)
    pressButton(STOP_GPIO_PIN)

#############
##API UTILS##
#############
def returnErrorStatus():
    return json.jsonify(
        ok=False
    )

def returnSuccessStatus():
    return json.jsonify(
        ok=True
    )

def filterEmptyPayload(httpRequest):
    content = httpRequest.get_json()
    if content is None:
        return returnErrorStatus()
    return content

#############
##API ROUTES#
#############
#define API routes
@app.route("/blinds", methods=['POST'])
#TODO:what if duration is not int
def blindControl():
    content = filterEmptyPayload(request)
    print "Incoming request: " + str(content)
    try                                             #Try to set the pin for the command, if not return error
        pin = pinsDict[content['command']]
    except KeyError:
        print "Error invalid or missing command: " + str(content['command'])
        return returnErrorStatus()
    pressButton(pin)
    if 'duration' in content:
        stopBlindsAfterDelay(content['duration'])
    return returnSuccessStatus()

# @app.route("/lights", methods=['POST'])
# def lightControl():
#     content = filterEmptyPayload(request)
