class Message:
     def __init__(self, info, position, race, correct):
          self.info = info
          self.position = position
          self.race = race
          self.color = 0
          self.correct = correct
          self.lose = False
          self.win = False