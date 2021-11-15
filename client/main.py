import socket

ClientSocket = socket.socket()
host = '127.0.0.3'
port = 1111

print('Waiting for connection')
try:
     ClientSocket.connect((host, port))
except socket.error as e:
     print(str(e))

Response = ClientSocket.recv(1024)
while True:
     # Regis until success
     while True:
          Input = input('Input your nickname: ')
          ClientSocket.send(str.encode(Input))
          Response = ClientSocket.recv(1024)
          
          if Response.decode('utf-8') == "Registration completed successfully":
               break

     # Wait for question
     while True:
          Response = ClientSocket.recv(1024)

          print(Response.decode('utf-8'))

          answer = input('Input the answer for this question: ')

          ClientSocket.send(str.encode(answer))

ClientSocket.close()