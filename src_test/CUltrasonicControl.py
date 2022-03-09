#-*- coding:utf-8 -*-

import os, time
if os.name == 'nt':
    import GPIO_Dummy as GPIO
else:
    import RPi.GPIO as GPIO


class CUltrasonicControl:
    def __init__(self):
        print("Start :", str(self))
        #self.initGpio()

    def __del__(self):
        pass

    def InitGpio(self, trig, echo):
        
        GPIO.setmode(GPIO.BCM)

        self.gpio_trig = trig
        self.gpio_echo = echo

        GPIO.setup(self.gpio_trig, GPIO.OUT)
        GPIO.setup(self.gpio_echo, GPIO.IN)
        
        print ("GPIO initialize", self.gpio_trig, self.gpio_echo)

    def GetDistance(self):
    
        GPIO.output(self.gpio_trig, False)
        time.sleep(0.5)

        GPIO.output(self.gpio_trig, True)
        time.sleep(0.00001)
        GPIO.output(self.gpio_trig, False)

        while GPIO.input(self.gpio_echo) == 0 :
            pulse_start = time.time()

        while GPIO.input(self.gpio_echo) == 1 :
            pulse_end = time.time()

        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17000
        distance = round(distance, 2)

        # print ("Distance : ", distance, "cm")
        return distance

    def APP_TEST_MODULE(self):
        trig = 13
        echo = 19
        self.InitGpio(trig, echo)
        try:
            while True :
                self.GetDistance()
                
        except KeyboardInterrupt:
            print('KeyboardInterrupt')

        except Exception as e:
            print('EXCEPTION:', e)

        finally:
            GPIO.cleanup()
            print("EXIT:", str(self))
            
    

if __name__ == "__main__":
    obj = CUltrasonicControl()
    obj.APP_TEST_MODULE()
