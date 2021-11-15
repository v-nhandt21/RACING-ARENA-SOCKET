class Player:
     def __init__(self, connection, ip, port, nickname):
          self.connection = connection
          self.ip = ip
          self.port = port
          self.position = 1
          self.nickname = nickname
          self.alive = True
          self.check3 = 0
          self.answer = None

     def check_consecutive_wrong(self):
          if self.check3 == 3:
               self.alive =False

     def check_win():
          a = 0

     def check_answer(a, b, operation, answer):
          a = 0

     def check_nickname():
          a = 0
          # a -> z , A -> Z, 0 -> 9 , _
          # Len <= 10
          # Check duplicate
