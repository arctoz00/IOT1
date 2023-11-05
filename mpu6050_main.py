from machine import I2C
from machine import Pin
from machine import PWM
from time import sleep
from mpu6050 import MPU6050
import sys
#Initialisering af I2C objekt
i2c = I2C(0,freq = 100000)     
#Initialisering af mpu6050 objekt
imu = MPU6050(i2c)

antal_taklinger = 0
####################################################################
BUZZ_PIN = 25
buzzer = PWM(Pin(BUZZ_PIN, Pin.OUT))

buzzer.duty(0)
state = False
while True:
    try:
        # printer hele dictionary som returneres fra get_values metoden
        imu_data = imu.get_values()

        print(imu_data["acceleration y"])
        
        value_y = imu_data["acceleration y"]
        if value_y > 7000 and state == False:
            print("Spiller står op")
            state = True
            
        if value_y < 6999 and state == True: 
            print("Spiller er taklet")
            antal_taklinger = antal_taklinger + 1
            state = False
            if antal_taklinger == 10:
                buzzer.duty(512)
                buzzer.freq(1000)
                sleep(5)
                buzzer.duty(0)
       
        print(antal_taklinger)
        
        sleep(0.5)
    except KeyboardInterrupt:
        print("Ctrl+C pressed - exiting program.")
        sys.exit()
