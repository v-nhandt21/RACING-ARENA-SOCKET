class Player:
     def __init__(self, connection, ip, port, nickname):
          self.connection = connection
          self.ip = ip
          self.port = port
          self.position = 1
          self.nickname = nickname
          self.alive = True
          self.check3fail = 0
          self.answer = None
          self.win = False

     def update_status(self, result, race):
          if self.answer == result:
               self.position += 1
               self.check3fail = 0
               if self.check_win(race):
                    self.win = True
               return True
          else:
               if self.position >= 1:
                    self.position -= 1
               self.check3fail += 1
               if self.check_consecutive_wrong():
                    self.alive =False
               return False

     def check_consecutive_wrong(self):
          if self.check3fail >= 3:
               return True
          else:
               return False

     def check_win(self, race):
          if self.postion >= race:
               return True
          else:
               return False