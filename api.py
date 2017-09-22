#load API frameworks
from flask import Flask
app = Flask(__name__)

#load GPIO framework and set correct pin layout
try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Error importing RPi.GPIO!  This is probably because you need superuser privileges.  You can achieve this by using 'sudo' to run your script")

if GPIO.getmode() == GPIO.BCM:
    print('BCM pin layout already set')
    pass
else:
    print('Setting pin layout mode')
    GPIO.setmode(GPIO.BCM)
#configure channels for blind control
UP_GPIO_PIN = 2
STOP_GPIO_PIN = 3
DOWN_GPIO_PIN = 4
chan_list = [UP_GPIO_PIN,STOP_GPIO_PIN,DOWN_GPIO_PIN]
GPIO.setup(chan_list,GPIO.OUT)

#define functions to control blinds via remote
def pressButton(pin):           #analogous to pressing up button
    GPIO.output(pin,GPIO.HIGH)  #power the pin
    GPIO.output(pin,GPIO.LOW)   #remove the power

def timedBlindMotion(pin, duration): #press directional button, then wait and press stop
    pressButton(pin)
    time.sleep(duration)
    pressButton(STOP_GPIO_PIN)

@app.route("/hello")
def hello():
    return "Hello World!"
@app.route("/up", methods=['POST'])
def up():
    return "Blinds up!"
@app.route("/down")
def down():
    return "Blinds down!"
@app.route("/stop")
def stop():
    return "Blinds stopped!"

#
#
#
# GPIO.setup(2,GPIO.OUT)
# GPIO.output(2,GPIO.HIGH)
# GPIO.output(2,GPIO.LOW)
