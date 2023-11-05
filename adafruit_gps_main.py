import sys
import umqtt_robust2 as mqtt
from mpu6050 import MPU6050
from machine import PWM
from machine import I2C
from machine import UART
from time import sleep
from gps_bare_minimum import GPS_Minimum
from machine import Pin, ADC
from battery_calc import battery_percentage
#########################################################################
# CONFIGURATION
gps_port = 2                               # ESP32 UART port, Educaboard ESP32 default UART port
gps_speed = 9600                           # UART speed, defauls u-blox speed
#########################################################################
# OBJECTS
uart = UART(gps_port, gps_speed)           # UART object creation
gps = GPS_Minimum(uart)                    # GPS object creation
#########################################################################
# OBJECTS til IMU
# i2c = I2C(0)
# imu = MPU6050(i2c)
# antal_taklinger = 0
# state = False
#########################################################################
# OBJECTS til Buzzer
BUZZ_PIN = 25
buzzer = PWM(Pin(BUZZ_PIN, Pin.OUT))
buzzer.duty(0)
#########################################################################
#LED objekt
GREEN_PIN = 23
#########################################################################
# kode som er udenfor loop 
led1 = Pin(GREEN_PIN, Pin.OUT)
led1.on()

buzzer.duty(512)
buzzer.freq(440)
sleep(5)
buzzer.duty(0)

########################################################################
def get_adafruit_gps():
    speed = lat = lon = None
    if gps.receive_nmea_data():
        # hvis der er kommet end bruggbar værdi på alle der skal anvendes
        if gps.get_speed() != -999 and gps.get_latitude() != -999.0 and gps.get_longitude() != -999.0:
            # returnerer data med adafruit gps format
            speed =str(gps.get_speed())
            lat = str(gps.get_latitude())
            lon = str(gps.get_longitude())
            return speed + "," + lat + "," + lon + "," + "0.0"
        else: # hvis ikke både hastighed, latitude og longtitude er korrekte 
            print(f"GPS data to adafruit not valid:\nspeed: {speed}\nlatitude: {lat}\nlongtitude: {lon}")
            return False
    else:
        return False
# Her kan i placere globale varibaler, og instanser af klasser



while True:
    try:
#         # printer hele dictionary som returneres fra get_values metoden
#         imu_data = imu.get_values()
# 
#         print(imu_data["acceleration y"])
#         
#         value_y = imu_data["acceleration y"]
#         if value_y > 7000 and state == False:
#             print("Spiller står op")
#             state = True
#             
#         if value_y < 6999 and state == True: 
#             print("Spiller er taklet")
#             antal_taklinger = antal_taklinger + 1
#             state = False
#             if antal_taklinger == 10:
#                 buzzer.duty(512)
#                 buzzer.freq(1000)
#                 sleep(5)
#                 buzzer.duty(0)
#        
#         print(antal_taklinger)
        #################################
        gps_data = get_adafruit_gps()
        gps_speed = gps.get_speed()
        # Hvis funktionen returnere en string er den True ellers returnere den False
        if gps_data: # hvis der er korrekt data så send til adafruit
            print(f'\ngps_data er: {gps_data}')
            mqtt.web_print(gps_data, 'Jesperj/feeds/mapfeed/csv')
            sleep(4)   
        #For at sende beskeder til andre feeds kan det gøres sådan:
            
            mqtt.web_print(gps_speed,'Jesperj/feeds/Speed')
            print("Speed er:", gps_speed)
        sleep(4) #Her bruges en funktionen batter_percentage() til at udregne batteri procenten
        mqtt.web_print(battery_percentage(), "Jesperj/feeds/batteri")
                   
        if len(mqtt.besked) != 0: # Her nulstilles indkommende beskeder
            mqtt.besked = ""            
        mqtt.sync_with_adafruitIO() # igangsæt at sende og modtage data med Adafruit IO
        print(".", end = '') # printer et punktum til shell, uden et enter        
    # Stopper programmet når der trykkes Ctrl + c
        sleep(4)
        
    except KeyboardInterrupt:
        print('Ctrl-C pressed...exiting')
        mqtt.c.disconnect()
        mqtt.sys.exit()ß