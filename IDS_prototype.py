import RPi.GPIO as GPIO
import time 
import datetime

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(18,GPIO.OUT)
GPIO.setup(4,GPIO.OUT)

current_time = datetime.datetime.now()

users = {"yeet":"1234","hapiz":"1234"}
status = ""
attempts = 3

def loginMenu(): 
	login =raw_input("Enter login name: ")
	passw =raw_input("Enter password: ")
	
	if login in users and users[login] == passw:
		print("Login Success,welcome %s" %(login))
		global status
		global attempts
		status="clear"
		attempts = 3
		
	else:
		print("\nIncorrect login details")
		status="not clear"
		attempts -= 1
		print "Attempts left:", attempts,"\n"

def measure():
    while True: 

        TRIG =23
        ECHO =24

        print "\nDistance Measurement in  Progress"

        GPIO.setup(TRIG,GPIO.OUT)
        GPIO.setup(ECHO,GPIO.IN)

        GPIO.output(TRIG,False)
        print ("waiting For Sensor")
        time.sleep(2)

        GPIO.output(TRIG,True)
        time.sleep (0.00001)
        GPIO.output(TRIG,False)

        while GPIO.input (ECHO)==0:
            pulse_start =time.time()

        while GPIO.input (ECHO)==1:
            pulse_end = time.time()

        pulse_duration = pulse_end - pulse_start

        distance = pulse_duration * 17150

        distance = round(distance, 2)

        if (distance<5):
            return
        else :
            GPIO.output(18,GPIO.LOW)
            GPIO.output(4,GPIO.LOW)
        print "Distance: ",distance, "cm"

		GPIO.cleanup()


while True :
	loginMenu()
	if status=="clear":
		break
	if attempts==0:
                print "Program exiting..."
		exit()	

while True and status=="clear":

    measure()
    timenow = current_time.strftime("%Y-%m-%d %H:%M")
    print "\n",timenow,"Intruder Alert !!! "
    sleeptime = 0

    while sleeptime <= 6.0:
        GPIO.output(18,GPIO.HIGH)
        GPIO.output(4,GPIO.HIGH)
        time.sleep(0.3)
        GPIO.output(18,GPIO.LOW)
        GPIO.output(4,GPIO.LOW)
        time.sleep(0.3)
        sleeptime += 0.6
    outF= open("intruderLog.txt","a")
    outF.write("\n")
    outF.write("Intrusion at ")
    outF.write(timenow)
    outF.close()	    


