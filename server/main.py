import socket
import os
from _thread import *
import random
import operator
import pickle
import time

from Player import Player
from Message import Message


ServerSocket = socket.socket()
host = ''
port = 1121
ServerSocket.bind((host, port))
print('Waitiing for a Connection..')
ServerSocket.listen(2)

PlayerList = []
MaxPlayer = 2
ThreadCount = 0
ROUND = 0

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
     global PlayerList
     global ROUND
     connection.send(str.encode('Welcome to the Server'))
     regis = False
     while regis == False:
          reply = "something"

          data = connection.recv(1020)
          nickname = data.decode('utf-8')
          print("Receive Player nickname: ",nickname)

          regis = True

          if len(nickname) > 10:
               regis = False
               reply = 'Nickname should be shorter than 10 characters'

          for char in nickname:
               if (char.isalnum() == False and char != '_'):
                    regis = False
                    reply = 'Invalid character.'
                    break
                    
          # check duplicate               
          if PlayerList != []:
               for player in PlayerList:
                    if player.nickname == nickname:
                         regis = False
                         reply = "Nickname existed"
                         break
          
          if regis == True:
               reply = 'ok'
               player = Player(connection, ip, port, nickname)
               PlayerList.append(player)

          connection.sendall(str.encode(reply))
          if regis:
               ROUND += 1
     # connection.close()

def play_round(connection, player, a, b, ops_char, idx):
     global ROUND
     
     player.timer = time.time()

     connection.sendall(str.encode(  str(a) + ops_char  + str(b)  ))
     player.answer = int(connection.recv(1020) )

     player.timer = time.time() - player.timer

     PlayerList[idx] = player
     ROUND += 1


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
               Client.sendall(str.encode("Full player"))
          if ThreadCount == MaxPlayer:
               break
     
     # Wait full login success
     print("Wait for all ready! ", end='')
     while ROUND != MaxPlayer:
          time.sleep(0.5)
          print('.', end='')

     # Race Lenght generate:
     race_length = input('Input length of the race: ')
     while not (race_length.isnumeric() and int(race_length)>3 and int(race_length)<26):
          race_length = input('Input length of the race again (3<race<26): ')
     race_length = int(race_length)

     while True:
          ROUND = 0
          # Question generate:
          a = random.randint(-10000,10000)
          b = random.randint(-10000,10000)
          operator = random.randrange(5)
          ops_char = operation(operator)
          ops_func = ops[ops_char]


          for idx, player in enumerate(PlayerList):
               start_new_thread(play_round, (player.connection, player, a, b, ops_char, idx ))
               print("Sent answer to ",player.nickname)

          print("Wait for all answers! ", end='')
          while ROUND != MaxPlayer:
               time.sleep(0.5)
               print('.', end='')
          print(".")

          fastest_timer = float('inf')
          fastest_player_id = None

          WinGame = False
          Bonus_Fastest = 0
          # check answer
          result = ops_func(a, b)
          # Update status
          for idx, player in enumerate(PlayerList):
               player.update_status(result, race_length)
          
               if player.timer < fastest_timer and player.correct:
                    fastest_timer = player.timer
                    fastest_player_id = idx

               if not player.correct:
                    Bonus_Fastest += 1

          if fastest_player_id != None:
               PlayerList[fastest_player_id].position += Bonus_Fastest - 1


          for player in PlayerList:
               player.info()
               if player.correct:
                    player.connection.sendall( pickle.dumps(Message("Correct Answer", player.position, player.race, player.correct)) )
               else:
                    player.connection.sendall( pickle.dumps(Message("Wrong Answer", player.position, player.race, player.correct)) )

               if not player.alive():
                    player.connection.sendall(str.encode(  "You were disqualified for having an accident 3 times in a row"  ))
               
               if player.win():
                    WinGame = True

          # Update alive
          PlayerList[:] = [ player for player in PlayerList if player.alive]

          # notification -> update infor
          if WinGame:
               for player in PlayerList:
                    if player.win():
                         player.connection.sendall(str.encode(  "You win the game"  ))
                    else:
                         player.connection.sendall(str.encode(  "You lose the game"  ))
               break # Newgame
          elif len(PlayerList) == 0:
               for player in PlayerList:
                    player.connection.sendall(str.encode(  "End game with no winner"  ))
               break # Newgame
          elif len(PlayerList) == 1:
               PlayerList[0].connection.sendall(str.encode(  "You win the game"  ))
               break

ServerSocket.close()