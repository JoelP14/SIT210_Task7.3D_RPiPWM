import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.OUT)
GPIO.setup(7, GPIO.OUT)

GPIO_TRIGGER = 16
GPIO_ECHO = 18
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

pwm = GPIO.PWM(12, 50)  # channel=12 frequency=50Hz
dc=0
pwm.start(dc)    

def Reverse(num):
    rev = 100
    num = rev - num
    print(num)
    return num

def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
 
    return distance

try:
	while 1:
		dist = distance() * 3 #used the multiplier to make it easier to demonstrate
		dc = dist
		dcreversed = Reverse(dc)
		print("Dist: " + str(dist))
		if dc < 100 and dc >= 0: #dc only accepts ranges within 0 and 100
			pwm.ChangeDutyCycle(dcreversed)
			time.sleep(0.1)
		else: #not within range
			dc = 0
			pwm.ChangeDutyCycle(dc)
			time.sleep(0.1)
except KeyboardInterrupt:
	GPIO.cleanup()

