#!/usr/bin/env python
import RPi.GPIO as GPIO
import os
import piggyphoto
import subprocess
GPIO.setmode(GPIO.BCM)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP) # input
GPIO.setup(18, GPIO.OUT) # LED
GPIO.setup(17, GPIO.OUT) # green led
savepath="./"
reconnnect=0

try:
#	cam=piggyphoto.camera()
	while 1:
	
		try:
			cam = piggyphoto.camera()
			print "Connected to Camera"
			GPIO.output(18,0)
			while 1:
				# switch on ready
				GPIO.output(17,1)
				# wait for button press
				GPIO.wait_for_edge(22, GPIO.RISING, bouncetime=100)
				# switch of green light
				GPIO.output(17,0)
				# shoot picture
				# upload picture
				received_image=1
				try:
					
					result = cam.capture_image()
					
				except piggyphoto.libgphoto2error as e:
					print e.message
					if(e.message.find("not complete operation")>0):
						print "Could not shoot image"
						received_image=0
					else:
						del cam
						raise
				
				if(received_image ==1):
					filename = result[1].lower()
					cam.download_file(result[0], result[1], savepath + filename)
					print "Uploading file.."
					subprocess.Popen(["./upload-and-remove.sh", filename])
					print "Return to main process"
					print "saved picture: "+filename
				
					info = cam._get_summary()
				# info = "bla"
				
					bat_ok = "Power status: on battery (power OK)"
					
					if(info.find(bat_ok) == -1) :
						print "Power not ok"
						GPIO.output(18,1)
					else:
						print "Power ok"
						GPIO.output(18,0)
					
	
		except piggyphoto.libgphoto2error as err:
			print "Connection to Camera lost or other error."
			GPIO.output(18,1)
			

except KeyboardInterrupt:
	print "Cleaning up"
except:
	print "Exception"
finally: 
	GPIO.cleanup()
