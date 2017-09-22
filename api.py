#load API frameworks
from flask import Flask
app = Flask(__name__)

#load GPIO framework and set correct pin layout
try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Error importing RPi.GPIO!  This is probably because you need superuser privileges.  You can achieve this by using 'sudo' to run your script")

UP_GPIO_PIN = 2
STOP_GPIO_PIN = 3
DOWN_GPIO_PIN = 4

#configure channels for blind control
def initPins():
    chan_list = [UP_GPIO_PIN,STOP_GPIO_PIN,DOWN_GPIO_PIN]
    GPIO.setup(chan_list,GPIO.OUT)

#cleanup pins
def resetPins():
    GPIO.cleanup()
    if GPIO.getmode() == GPIO.BCM:
        print('BCM pin layout already set')
        pass
    else:
        print('Setting pin layout mode')
        GPIO.setmode(GPIO.BCM)

#define button presses
def pressButton(pin):                        #analogous to pressing up button
    GPIO.output(pin, (GPIO.HIGH, GPIO.LOW))  #power the pin then remove the power

def timedBlindMotion(pin, duration): #press directional button, then wait and press stop
    pressButton(pin)
    time.sleep(duration)
    pressButton(STOP_GPIO_PIN)

resetPins()
#define API routes
@app.route("/blinds", methods=['POST'])
def blindControl():

    # client_id = request.args.get('client_id', '')
    # client_secret = request.args.get('client_secret', '')
