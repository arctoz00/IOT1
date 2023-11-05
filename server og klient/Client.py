from socket import *

serverName = ' skriver servers IP'
serverPort = 12005
clientSocket = socket(AF_INET, SOCK_DGRAM)

print ()
print ("-----------------------------")
print ("Klienten er klar til at sende")
print ("-----------------------------")
print ()
print ()

while True:
    message = input(' Skriver noget til serveren: ')
    clientSocket.sendto(message.encode(),(serverName, serverPort))