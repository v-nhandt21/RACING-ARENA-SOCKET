import socket, pickle

ClientSocket = socket.socket()
host = '127.0.0.1'
port = 1121

print('Waiting for connection')
ClientSocket.connect((host, port))

Response = ClientSocket.recv(1020)
print(Response.decode('utf-8'))

while True:
     # Regis until success
     LoginSuccess = False
     while not LoginSuccess:
          Input = input('-> Input your nickname: ')
          ClientSocket.send(str.encode(Input))

          Response = ClientSocket.recv(1020)
          
          if Response.decode('utf-8') == "ok":
               print("Registration completed successfully")
               LoginSuccess = True
          else:
               print(Response.decode('utf-8'))

     print("Wait for another player")
     # Wait for question
     while True:
          Response = ClientSocket.recv(1020)

          print(Response.decode('utf-8'))

          answer = input('-> Input the answer for this question: ')

          ClientSocket.send(str.encode(answer))

          print("-> Wait for another racer!")

          Result = ClientSocket.recv(1020)

          print(Result.decode('utf-8'))

          print("==============================")
          print("Next round")


ClientSocket.close()