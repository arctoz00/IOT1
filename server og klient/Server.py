from socket import*
import datetime
serverPort = 12005
serverSocket = socket( AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))

y = datetime.datetime.now() # tager en tid når man begyder serveren
("The time is now : = %s:%s:%s" % (y.hour, y.minute, y.second))

print ()
print("-------------------------------")
print("Serveren er klar til at modtage")
print("-------------------------------")
print()
print()

while True:
    message, klient = serverSocket.recvfrom (2048)
    print(message.decode()) # Skriver beskeden der er sendt fra klient
    print ()
    print ("IP/port= ", klient)#Skriver IP-adressen og port nummer af klienten.
    x = datetime.datetime.now()#Finder tid på hvornår der er sendt besked
    ("The time is now: %s:%s:%s" % (x.hour, x.minute, x.second))
    
    tidspunkt = x - y
    print(tidspunkt)

