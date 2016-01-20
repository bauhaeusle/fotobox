import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # input
#GPIO.setup(24, GPIO.OUT) # LED

try:
	print "hallo"
	while 1:
		GPIO.wait_for_edge(4, GPIO.RISING, bouncetime=100)
		print "rising edge"


except KeyboardInterrupt:
	print "Keyboard Interrupt"
except:
	print "Exception"
finally:
	GPIO.cleanup()
