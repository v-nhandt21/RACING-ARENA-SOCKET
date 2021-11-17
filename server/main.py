import socket
import os
from Player import Player
from _thread import *
import random

ServerSocket = socket.socket()
host = '127.0.0.3'
port = 1111
ThreadCount = 0
try:
     ServerSocket.bind((host, port))
except socket.error as e:
     print(str(e))

print('Waitiing for a Connection..')
ServerSocket.listen(2)

PlayerList = []
MaxPlayer = 2

          # a -> z , A -> Z, 0 -> 9 , _
          # Len <= 10
          # Check duplicate

def login_client(connection, ip, port):
     connection.send(str.encode('Welcome to the Server'))
     while True:

          data = connection.recv(2048)
          # check duplicate
          regis = True
          nickname = data.decode('utf-8')
          for char in nickname:
               if char.isalnum() == False and char != '_':
                    reply = 'Invalid character. Type nickname again: '
                    regis = False
                    break
          if PlayerList != []:
               for player in PlayerList:
                    if player.nickname == nickname:
                         regis = False
                         break
          
          if regis == True:
               reply = 'Registration completed successfully'
          else:
               reply = 'Choose another nickname: '

          if not data:
               break
          connection.sendall(str.encode(reply))

          if regis == True:
               player = Player(connection, ip, port, nickname)
               PlayerList.append(player)
               break
     # connection.close()

while True:
     
     # Wait full player
     while True:
          Client, address = ServerSocket.accept()
          print('Connected to: ' + address[0] + ':' + str(address[1]))

          if ThreadCount < MaxPlayer:
               ThreadCount += 1
               print('Player Number: ' + str(ThreadCount))
               start_new_thread(login_client, (Client, address[0], address[1] ))
               
          else:
               print(PlayerList)
               a = 0 #TODO: Reponse you khong connect duoc nghe may
          if ThreadCount == MaxPlayer:
               break

     # Race Lenght generate:
     race_lenght = input('Input length of the race: ')

     while True:
          # Question generate:
          a = random.randint(-10000,10000)
          b = random.randint(-10000,10000)
          operator = random.randrange(6)

          # Send question
          print(str.encode(  str(a) + str(operator)  + str(b)  ))

          for player in PlayerList:
               player.connection.sendall(str.encode(  str(a) + str(operator)  + str(b)  ))

          fastest = -1

          # Receive answer
          for player in PlayerList:
               player.answer = int( player.connection.recv(2048) )

          # check answer
          for player in PlayerList:
               print(player.answer)

          # check status user 

          # notification -> update infor

ServerSocket.close()