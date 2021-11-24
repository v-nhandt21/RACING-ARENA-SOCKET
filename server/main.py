import socket
import os, sys
from _thread import *
import random
import operator
import pickle
import time

from Player import Player

PlayerList = []
MaxPlayer = 2
MaxTime = None
ThreadCount = 0
ROUND = 0

ops = ops = {
     "+": operator.add,
     "-": operator.sub,
     "*": operator.mul,
     "/": operator.floordiv,
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
     global MaxPlayer
     global PlayerList
     global ROUND
     global MaxTime

     connection.send(str.encode('Welcome to the Server'+"_"+str(MaxPlayer) +"_"+str(MaxTime)))
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
               reply = 'ok_' + str(len(PlayerList))
               player = Player(connection, ip, port, nickname, color=len(PlayerList))
               PlayerList.append(player)

          connection.sendall(str.encode(reply))
          if regis:
               ROUND += 1
     # connection.close()

def play_round(connection, player, a, b, ops_char, idx):
     global ROUND
     global PlayerList
     
     player.timer = time.time()

     connection.sendall(str.encode(  str(a) + ops_char  + str(b)  ))

     answer = connection.recv(1020).decode('utf-8')

     print(player.info)

     player.answer = int(answer)

     player.timer = time.time() - player.timer
     PlayerList[idx] = player
     ROUND += 1

def init_game(connection, race):
     global ROUND
     connection.sendall(str.encode(str(race)))
     _ = connection.recv(1020)
     ROUND += 1

def update_status(connection, Message):
     global ROUND
     connection.sendall(str.encode(Message))
     _ = connection.recv(1020)
     ROUND += 1

def Game_Server(port = 1123, host = ''):

     global PlayerList
     global MaxPlayer
     global MaxTime
     global ThreadCount
     global ROUND

     while True:

          while True:
               MaxPlayer = int(input('-> Input max player (from 2 to 10 players): '))
               if MaxPlayer >= 2 and MaxPlayer <=10:
                    break

          while True:
               MaxTime = int(input('-> Input max time (from 10 to 15 seconds): '))
               if MaxTime >= 10 and MaxTime <=15:
                    break

          print("Maxplayer is set: ", MaxPlayer)
          print("Maxtime is set: ", MaxTime)
          
          ServerSocket = socket.socket()
          port += 1
          ServerSocket.bind((host, port))
          print('Waitiing for a Connection..')
          ServerSocket.listen(2)

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

          for idx, player in enumerate(PlayerList):
               start_new_thread(init_game, (player.connection,race_length))

          # Wait for all ready
          ROUND = 0
          while ROUND != MaxPlayer:
               time.sleep(0.5)

          while True:
               print(">"*40)

               Alive = 0
               ROUND = 0
               # Question generate:
               a = random.randint(-10,10)
               operator = random.randrange(5)
               if operation == 3 or operation == 4:
                    b = random.randint(-10,10) 
                    while b==0:
                         b = random.randint(-10,10) 
               else:
                    b = random.randint(-10,10)               
               ops_char = operation(operator)
               ops_func = ops[ops_char]

               result = ops_func(a, b)
               print("Result: ",result)       

               for idx, player in enumerate(PlayerList):
                    if player.alive:
                         Alive += 1
                         start_new_thread(play_round, (player.connection, player, a, b, ops_char, idx ))

               print("Wait for all answers! ", end='')
               while ROUND != Alive:
                    time.sleep(0.5)

               fastest_timer = float('inf')
               fastest_player_id = None

               WinGame = False
               Bonus_Fastest = 0
               

               # Update status
               for idx, player in enumerate(PlayerList):
                    if player.alive:
                         player.update_status(result, race_length)
                    
                         if player.timer < fastest_timer and player.correct:
                              fastest_timer = player.timer
                              fastest_player_id = idx

                         if player.correct == False:
                              Bonus_Fastest += 1

               if fastest_player_id != None and Bonus_Fastest>0:
                    PlayerList[fastest_player_id].position += Bonus_Fastest - 1

               Message = []

               for player in PlayerList:
                    player.info()

                    if not player.alive:
                         Message.append(-100)
                    elif player.win:
                         Message.append(100)
                         WinGame = True
                    else:
                         Message.append(player.position)

               print(Message)
               Message = [str(s) for s in Message]
               Message = "_".join(Message)

               for idx, player in enumerate(PlayerList):
                    if player.alive:
                         start_new_thread(update_status, (player.connection, Message) )

               # Wait for all ready
               ROUND = 0
               while ROUND != MaxPlayer:
                    time.sleep(0.5)

               # Update alive
               # PlayerList[:] = [ player for player in PlayerList if player.alive]

               # notification -> update infor
               if WinGame:
                    print("Game have the winner")
                    break # Newgame
               if Alive == 0:
                    print("You are all loser!")
                    break

          print("+++++++++++++++++++++++++++++++++")
          print("====== Game End - Next Race =====")

     ServerSocket.close()

if __name__ == '__main__':
     if len(sys.argv) == 2:
          port = int(sys.argv[1])
          Game_Server(port)
     else:
          Game_Server()