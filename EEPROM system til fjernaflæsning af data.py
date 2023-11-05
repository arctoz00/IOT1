import sys, uselect
from machine import UART

#CONFIGUARTION
#Remote

uart_remote_portv = 1
uart_remote_pin_tx = 33
uart_remote_pin_rx = 32
uart_remote_speed = 9600

# User data
group_id = 99

# OBJECTS
uart_remote = UART (uart_remote_port, baudrate = uart_remote_speed, tx = uart_remote_pin_tx, rx = uart_remote_pin_rx)#Remote UART object

usb = uselect.poll()
usb.register(sys.stdin, uselect.POLLIN)
########################################################################################################################
#Functions



########################################################################################################################
#PROGRAM
print("Two-waz ESP32 remote data system\n")

while True:
    # Recive commands from and send responses to the UART
    if uart_remote.any()> 0:
        string = uart_remote.read().decode()
        string = string.strip()
        print("Remote: " + string)
        
    # Recive user input from the USB and send commands to the UART
    if usb.poll(0):
       string = sys.stdin.readline()
       sys.stdin.readline()
       string = string.strip()
       print("USB   : " + string)
    
       uart_remote.write(string + "\n")

