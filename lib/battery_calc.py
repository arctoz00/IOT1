from machine import ADC, Pin

analog_pin = ADC(Pin(34))
analog_pin.atten(ADC.ATTN_11DB)


def battery_percentage():
    bat_measure = 3.3 / 4095
    min_volt = 3.0
    max_volt = 4.2
    analog_val = analog_pin.read()
    print ( "Analif målt værdi: ", analog_val)
    #målt:
    spænding = analog_val * bat_measure + 0.15 #Esp starter med at måle fra 0,15 volt af 
    print ("spænding er: ", spænding)

    Ubat = 3.95
    Upin = 1.40

    bo_er_go = Ubat / Upin

    Batsp=bo_er_go * spænding

    print("Batsp:",Batsp)

    Batpct = 83.33 * Batsp -250
    print("Batpct:",Batpct)
    return Batpct
      