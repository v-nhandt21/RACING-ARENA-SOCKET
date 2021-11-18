import socket
import os
from Player import Player
from _thread import *
import random
import operator

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

ops = ops = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv,
    "%": operator.mod
}

def operation(i):
     switcher={
                0:'+',
                1:'-',
                2:'*',
                3:'/',
                4:'%',
               }
     return switcher.get(i)   

def login_client(connection, ip, port):
     connection.send(str.encode('Welcome to the Server'))
     while True:

          data = connection.recv(2048)
          nickname = data.decode('utf-8')
          
          regis = False
          # check nickname
          while regis == False:
               for char in nickname:
                    if (char.isalnum() == False and char != '_') or len(nickname) > 10:
                         reply = 'Invalid character. Type nickname again: '
                         data = connection.recv(2048)
                         nickname = data.decode('utf-8')
                         
               # check duplicate               
               if PlayerList != []:
                    for player in PlayerList:
                         if player.nickname == nickname:
                              regis = False
                         else:
                              PlayerList.append(nickname)
                              break
          
          if regis == True:
               reply = 'Registration completed successfully'
               
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
     race_length = input('Input length of the race: ')

     while True:
          # Question generate:
          a = random.randint(-10000,10000)
          b = random.randint(-10000,10000)
          operator = random.randrange(5)
          ops_char = operation(operator)
          ops_func = ops[ops_char]

          # Send question
          print(str.encode(  str(a) + ops_char  + str(b)  ))

          for player in PlayerList:
               player.connection.sendall(str.encode(  str(a) + ops_char  + str(b)  ))

          fastest = -1

          # Receive answer
          for player in PlayerList:
               player.answer = int( player.connection.recv(2048) )

          # check answer
          result = ops_func(a, b)
          for player in PlayerList:
               if player.answer == result:
                    player.answer += 1
               elif player.check3 < 3:
                    if player.position != 1:
                         player.position -= 1
                    player.check3 += 1
                    
          # check status user
          for player in PlayerList:
               if player.check3 == 3:
                    PlayerList.remove(player) 

          # notification -> update infor

ServerSocket.close()