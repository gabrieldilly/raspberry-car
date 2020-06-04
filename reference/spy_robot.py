from flask import *
import RPi.GPIO as GPIO
import subprocess
import shlex

p=subprocess.Popen(shlex.split('./mjpg_streamer -o "output_http.so -w ./www" -i "input_raspicam.so"'))

app=Flask(__name__)
GPIO.setmode(GPIO.BCM)
motor_array = [6,5,19,13]
for pin in motor_array:
    GPIO.setup(pin, GPIO.OUT)
motorL1_pwm = GPIO.PWM(6, 100)
motorL2_pwm = GPIO.PWM(5, 100)
motorR1_pwm = GPIO.PWM(19, 100)
motorR2_pwm = GPIO.PWM(13, 100)
motorL1_pwm.start(0)
motorL2_pwm.start(0)
motorR1_pwm.start(0)
motorR2_pwm.start(0)

def turn_wheel(motor1, motor2):
    motor1 = motor1 / 2
    motor2 = motor2 / 2
    
    if motor1<0:
        motorL2_pwm.ChangeDutyCycle(motor1*-1)
        motorL1_pwm.ChangeDutyCycle(0)#make positive if negative
    else:
        motorL1_pwm.ChangeDutyCycle(motor1)
        motorL2_pwm.ChangeDutyCycle(0)
        
    if motor2<0:
        motorR2_pwm.ChangeDutyCycle(motor2*-1)
        motorR1_pwm.ChangeDutyCycle(0)#make positive if negative
    else:
        motorR1_pwm.ChangeDutyCycle(motor2)
        motorR2_pwm.ChangeDutyCycle(0)

@app.route("/control/", methods=['GET','POST'])
def control():
    data = request.get_json()
    motor1 = data['motor1']
    motor2 = data['motor2']
    turn_wheel(motor1, motor2)
    print("Motor 1 value is: "+str(motor1)+", motor 2 value is: "+str(motor2))
    return "yay"
if __name__=="__main__":
    try:
        app.run(host='0.0.0.0')
    except KeyboardInterrupt: 
        p.terminate()
        pass
