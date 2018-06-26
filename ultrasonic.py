import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)


def ultra():
        TRIG=23
        ECHO=24
        GPIO.setup(TRIG,GPIO.OUT)
        GPIO.setup(ECHO,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
        GPIO.output(TRIG, False)
        GPIO.output(TRIG, True)
        time.sleep(0.00001)
        GPIO.output(TRIG, False)
        while GPIO.input(ECHO)==0:
            pulse_start=time.time()

        while GPIO.input(ECHO)==1:
            pulse_end=time.time()
        pulse_duration=pulse_end-pulse_start

        distance=pulse_duration*17150

        distance=round(distance,2) 

        
        
        return distance
