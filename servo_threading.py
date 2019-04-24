
from flask import Flask
from flask_ask import Ask, statement, convert_errors
import RPi.GPIO as GPIO
import time
import threading
import thread
import logging

flag = 1
GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.OUT)
p = GPIO.PWM(12, 1)
app = Flask(__name__)
ask = Ask(app, '/')

logging.getLogger("flask_ask").setLevel(logging.DEBUG)

def gpio_status(status):
    if status in ['on','high' ]:
        p.start(.1)
        try:
            while flag == 1:
                p.ChangeDutyCycle(.1)  # turn towards 90 degree
                #@ask.intent('GpioIntent', mapping={'status': 'status'})
                # if status in ['off','low' ]:
                    # p.stop()
                    # GPIO.cleanup()
                    # return statement('Turning off servo')
                # else:
                    # continue
            p.stop()
            GPIO.cleanup()
            flag = 1
        except KeyboardInterrupt:
            p.stop()
            GPIO.cleanup()
        return statement('Turning servo off')
    else:
        return statement('did not ask to turn on')

def flag(status):
	if status in ['off']:
		flag = 0

@ask.intent('GpioIntent', mapping={'status': 'status'})
def threads(status):
    try:
        thread.start_new_thread(gpio_status, (status))
        thread.start_new_thread(flag, (status))
    except KeyboardInterrupt:
                p.stop()
                GPIO.cleanup()
@ask.intent('AMAZON.StopIntent')
def stop():
    bye_text = render_template('bye')
    return statement(bye_text)

if __name__ == '__main__':
    port = 5000 #the custom port you want
    app.run(host='0.0.0.0', port=port)


