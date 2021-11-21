import socket, pickle, time, sys

def Game_Client(port = 1123, host = '127.0.0.1'):
     ClientSocket = socket.socket()     

     print('Waiting for connection')
     ClientSocket.connect((host, port))

     Response = ClientSocket.recv(1020).decode('utf-8')
     welcom, max_player, max_time = Response.split("_")

     MaxPlayer = int(max_player)
     MaxTime = int(max_time)
     Color = None
     Race_Len = None
     Last_Status = 1

     while True:
          # Regis until success
          LoginSuccess = False
          while not LoginSuccess:
               Input = input('-> Input your nickname: ')
               ClientSocket.send(str.encode(Input))

               Response = ClientSocket.recv(1020)
               
               if Response.decode('utf-8')[:2] == "ok":
                    Color = int(Response.decode('utf-8').split("_")[1])
                    print("Registration completed successfully with order: ", Color)
                    LoginSuccess = True
               else:
                    print(Response.decode('utf-8'))

          ###############################
          print("Wait for another player")
          race_len = ClientSocket.recv(1020)
          Race_Len = int(race_len)

          # => Reader Game UI
          time.sleep(2)

          print("Racer boiz, you got "+ str(Race_Len)  + " round")
          ClientSocket.send(str.encode("Ready"))
          ################################

          # Wait for question
          while True:
               Response = ClientSocket.recv(1020)

               print(Response.decode('utf-8'))

               answer = input('-> Input the answer for this question: ')

               ClientSocket.send(str.encode(answer))

               print("-> Wait for another racer!")

               Message = ClientSocket.recv(1020).decode('utf-8')

               print(Message)
               Status = Message.split("_")
               Status = [int(s) for s in Status]

               MyStatus = Status[Color]

               if MyStatus == -3:
                    print("You have losed the race!")
               elif MyStatus == 100:
                    print("You have win the race!")
               else:
                    if MyStatus == Last_Status + 1:
                         print()
                    elif MyStatus == Last_Status - 1:
                         print()
                    elif MyStatus > Last_Status:
                         print("Bonus for Fastest Racer in this round")

               Last_Status = MyStatus

               # check alive, correct, win, ...
               ClientSocket.send(str.encode("Next question"))
               print("==============================")
               print("Next round")

     ClientSocket.close()

if __name__ == '__main__':

     if len(sys.argv) == 2:
          port = int(sys.argv[1])
          Game_Client(port=port)
     else:
          Game_Client()