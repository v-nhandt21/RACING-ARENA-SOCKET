class Player:
     def __init__(self, connection, ip, port, nickname, color):
          self.connection = connection
          self.ip = ip
          self.port = port
          self.position = 1
          self.nickname = nickname
          self.alive = True
          self.check3fail = 0
          self.answer = None
          self.win = False
          self.timer = 0
          self.color = color
          self.correct = False

     def info(self):
          print("*****************************")
          print("Position: ",self.position)
          print("Nickname: ",self.nickname)
          # print("Alive: ", self.alive)
          print("Wrong 3 times: ",self.check3fail)
          # print(self.answer)
          print("Winner: ",self.win)
          # print(self.timer)
          # print(self.color)
          print("Correct: ",self.correct)
          print("*****************************")

     def update_status(self, result, race):
          if self.answer == result:
               self.position += 1
               self.check3fail = 0
               if self.check_win(race):
                    self.position = 100
                    self.win = True
               self.correct = True
          else:
               if self.position > 1:
                    self.position -= 1
               self.check3fail += 1
               if self.check_consecutive_wrong():
                    self.alive =False
               self.correct = False

     def check_consecutive_wrong(self):
          if self.check3fail == 3:
               return True
          else:
               return False

     def check_win(self, race):
          if self.position > race:
               return True
          else:
               return False