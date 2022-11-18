#-*- coding:utf-8 -*-

import os, time
if os.name == 'nt':
    import GPIO_Dummy as GPIO
else:
    import RPi.GPIO as GPIO  # sudo pip3 install RPi.GPIO     // sudo apt-get install python3-dev  pi@raspberrypi:~ $ sudo apt-get install python3-rpi.gpio


class CGpioControl:
    def __init__(self, pin_list):
        print("Start :", str(self))
        
        self.pin_list = pin_list
        self.InitGpio()
    def __del__(self):
        pass

    def InitGpio(self):

        GPIO.setmode(GPIO.BCM)
        for pin in self.pin_list:
            GPIO.setup(pin, GPIO.OUT)
            #GPIO.setup(pin, GPIO.OUT, pull_up_down = GPIO.PUD_UP)
            print ("pin = ", pin, "GPIO.OUT")

        #self.SetAllLed(False)
        self.SetDoorLock(False)


    def SetDoorLock(self, stat):
        if stat == "on":
            stat = False
        else:
            stat = True

        for pin in self.pin_list:
            GPIO.output(pin, stat)



if __name__ == "__main__":
    obj = None
    try:
        #while(True):
            list_pin = []
            list_pin = []
            obj = CGpioControl(list_pin)
            obj.APP_MAIN()

    except KeyboardInterrupt:
        print('KeyboardInterrupt')

    except Exception as e:
        print('EXCEPTION:', e)

    finally:
        GPIO.cleanup()
        print("EXIT:", str(obj))



