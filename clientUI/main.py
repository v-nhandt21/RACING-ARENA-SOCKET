import socket, pickle, time, sys
import pygame
from sys import  exit
import sys



def Game_Client(port = 1123, host = '127.0.0.1'):
     ClientSocket = socket.socket()     

     print('Waiting for connection')
     ClientSocket.connect((host, port))

     Response = ClientSocket.recv(1020).decode('utf-8')
     welcom, max_player, max_time = Response.split("_")

     def display_time():
          current_time = int((pygame.time.get_ticks() / 1000)-starttime)

          time = base_font.render("{}\{}".format(current_time,max_time) , False, 40)
          time_rect = time.get_rect(center=(width - 75, height - 50))
          screen.blit(time, time_rect)
          return current_time
     pygame.init()
     base_font = pygame.font.Font(None, 32)

     MaxPlayer = int(max_player)

     if (MaxPlayer < 5):
          height = 5 * 80
     else:
          height = MaxPlayer * 80
     width=1200
     starttime=0
     clock = pygame.time.Clock()

     screen = pygame.display.set_mode((width, height))
     pygame.display.set_caption('Racing Arena')
     bottom = pygame.Surface((width, height / MaxPlayer + 80))
     bottom.fill('white')
     Race = pygame.Surface((width, height))
     Race = pygame.transform.scale(Race, (width, height))
     Race.fill('#75E6DA')
     Background=pygame.image.load('background.png')
     Background=pygame.transform.scale(Background,(width,height))
     carRed=pygame.image.load('car/car1.png')
     carRed=pygame.transform.scale(carRed,(80,40))
     blackCar=pygame.image.load('car/blackcar1.png')
     blackCar = pygame.transform.scale(blackCar, (80, 40))
     grayCar=pygame.image.load('car/graycar.png')
     grayCar = pygame.transform.scale(grayCar, (80, 40))
     carwhite=pygame.image.load('car/carwhite.png')
     carwhite=pygame.transform.scale(carwhite,(80,40))
     cargreen = pygame.image.load('car/cargreen.png')
     cargreen=pygame.transform.scale(cargreen,(80,40))
     blueCar = pygame.image.load('car/bulecar.png')
     blueCar = pygame.transform.scale(blueCar, (80, 40))
     YellowCar=pygame.image.load('car/yellowcar.png')
     YellowCar=pygame.transform.scale(YellowCar,(80,40))
     CyanCar=pygame.image.load('car/cyancar.png')
     CyanCar=pygame.transform.scale(CyanCar,(80,40))
     MagentaCar=pygame.image.load('car/MagentaCar.png')
     MagentaCar=pygame.transform.scale(MagentaCar,(80,40))
     BrownCar=pygame.image.load('car/brownCar.png')
     BrownCar=pygame.transform.scale(BrownCar,(80,40))





     line = pygame.Surface((width, 10))
     line.fill('black')

     player = [carRed, blackCar, grayCar, carwhite, cargreen, blueCar, YellowCar, CyanCar, MagentaCar, BrownCar]
     playercolors = ['red', 'black', 'gray', 'white', 'green', 'blue', 'yellow', 'cyan', 'megenta', 'brown']
     #assgin rect for each player
     player_rect = []
     for i in range(MaxPlayer):
          player_r = player[i].get_rect(midbottom=(50, (height - 100) - ((height - 100) / MaxPlayer) * i))
          player_rect.append(player_r)
     position = [1 for i in range(MaxPlayer)]
     lastposition=[0 for i in range(MaxPlayer)]

     # nickname register
     base_font = pygame.font.Font('Pixeltype.ttf', 40)
     user_text = ''
     input_rect = pygame.Rect(width / 2 - 100, height / 2 - 16, 200, 32)
     name_rect = pygame.Rect(50, height - 70, 200, 40)

     # Register
     Register = base_font.render("Choose your nickname.", False, 'Black')
     Register_rect = Register.get_rect(center=(width / 2, height / 2 - 50))
     RegisterS = base_font.render("Registration Completed Successfully", False, 'Black')
     RegisterS_rect = RegisterS.get_rect(center=(width / 2, height / 2 + 50))
     Invalidchartext = base_font.render("Invalid character.", False, 'Black')
     Invalidchartext_rect = Invalidchartext.get_rect(center=(width / 2, height / 2 + 50))
     NameExistText = base_font.render("Nickname existed", False, 'Black')
     NameExistText_rect = NameExistText.get_rect(center=(width / 2, height / 2 + 50))
     # name

     # Quizz
     quizzSur = pygame.image.load('quizz1.jpg').convert()
     quizzSur = pygame.transform.scale(quizzSur, (quizzSur.get_width() - 10, quizzSur.get_height() - 10))
     quizzSur_rect = quizzSur.get_rect(center=(width / 2, (height - 100) / 2))




     # answer
     AnswerE = pygame.image.load('answer.jpg').convert()
     AnswerE = pygame.transform.scale(AnswerE, (AnswerE.get_width() / 6, AnswerE.get_height() / 6))
     AnswerE_rect = AnswerE.get_rect(midtop=(width / 2, height - 90))

     AnswerBox = pygame.image.load('answerbox.jpg').convert()
     AnswerBox_rect = AnswerBox.get_rect(midbottom=(width / 2, height))

     answer = ''

     #winGame
     Win_font=pygame.font.Font('Pixeltype.ttf',64)
     WinText=Win_font.render("Game Over!! You win the race",False,'Red')
     WinText_rect=WinText.get_rect(center=(width/2,height/2))
     background=pygame.Surface((width,height),pygame.SRCALPHA).convert_alpha()


     #loseGame
     LoseText = Win_font.render("Game Over!! You lose the race", False, 'Red')
     LoseText_rect = LoseText.get_rect(center=(width / 2, height / 2))

     QuitTex=Win_font.render("Press Q to quit!!",False,'Red')
     QuitTex_rect=QuitTex.get_rect(center=(width/2,height/2+50))






     gameActive = False
     nickName = True
     Quizz = False
     wait=False
     InvalidChar=False
     firstQuest=False
     waitAnswer=False
     FishishMoving=[0 for i in range(MaxPlayer)]
     winGame=False
     loseGame=False
     NickNameExisted=False


     MaxTime = int(max_time)
     Color = None
     Race_Len = None
     Last_Status = 1
     waittime=0


     while True:

          print(answer)
          for event in pygame.event.get():
               if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
               if event.type == pygame.KEYDOWN:
                    # postion event
                    if winGame or loseGame:
                         if event.key==pygame.K_q:
                              ClientSocket.close()
                              pygame.quit()
                              exit()
                    # Answer input event
                    if event.key == pygame.K_SPACE and Quizz and gameActive and nickName == False:
                         if answer=="":
                              answer="-1000000"

                         ClientSocket.send(str.encode(answer))
                         waitAnswer=True


                         Quizz = False
                         answer = ""


                    if event.key == pygame.K_SPACE and nickName and wait==False:
                         Input=user_text
                         ClientSocket.send(str.encode(Input))

                         Response = ClientSocket.recv(1020)
                         if Response.decode('utf-8')[:2] == "ok":
                              Color = int(Response.decode('utf-8').split("_")[1])
                              print("Registration completed successfully with order: ", Color)

                              wait = True
                              InvalidChar = False
                              NickNameExisted=False



                         elif Response.decode('utf-8')=='Invalid character.':
                              InvalidChar=True
                              NickNameExisted=False

                         elif Response.decode('utf-8')=='Nickname existed':
                              InvalidChar=False
                              NickNameExisted=True










                    if wait==False:
                         if event.key == pygame.K_BACKSPACE and nickName:
                              user_text = user_text[0:-1]
                         else:
                              if (len(user_text)) < 10 and nickName:
                                   user_text += event.unicode


                    # quizz input

                    if event.key == pygame.K_BACKSPACE and Quizz and gameActive:

                         answer = answer[0:-1]

                    else:
                         if Quizz and gameActive:
                              answer += event.unicode

          ###############################
          #print("Wait for another player")



          screen.blit(Race, (0, 0))


          if waitAnswer:
               ClientSocket.setblocking(False)

               try:
                    Message = ClientSocket.recv(1020).decode('utf-8')
                    Status = Message.split("_")
                    Status = [int(s) for s in Status]
                    position=Status
                    MyStatus = Status[Color]
                    if 100 in position:
                         Quizz=False
                         if(MyStatus==100):
                              print('WinGame')

                              winGame=True

                         else:
                              loseGame=True

                    if MyStatus==-100:
                         Quizz=False
                         loseGame=True




                    waitAnswer=False
                    ClientSocket.setblocking(True)


               except:
                    pass


          if nickName == True:
               starttime = int(pygame.time.get_ticks() / 1000)

          if Quizz == False and gameActive == True:
               starttime = int(pygame.time.get_ticks() / 1000)

          if gameActive:
               screen.blit(bottom, (0, height - 100))

               screen.blit(AnswerE, AnswerE_rect)
               screen.blit(AnswerBox, AnswerBox_rect)
               step = (width)/(Race_Len)


               for i in range(MaxPlayer):

                    screen.blit(line, (0, (height - 100) - ((height - 100) / MaxPlayer) * i))

                    if waitAnswer == False and Quizz==False :
                         if position[i]==-100:
                              FishishMoving[i]=1
                         else:
                              if (player_rect[i].right < (position[i] - 1) * step+50):
                                   player_rect[i].right += 1
                              elif (player_rect[i].left > (position[i] - 1) * step+50):
                                   player_rect[i].left -= 1
                              else:
                                   FishishMoving[i]=1
                         if sum(FishishMoving)==MaxPlayer :
                              for i in range(MaxPlayer):
                                   FishishMoving[i]=0
                              ClientSocket.send(str.encode("Next question"))
                              Quizz = True
                              firstQuest = True





                    screen.blit(player[i], player_rect[i])




               name = base_font.render(user_text, True, 'black')

               name_rect.w = name.get_width() + 20
               # colors background of player
               playerColorbottom = pygame.Rect(0, height - 90, name_rect.right + 50, 100)
               pygame.draw.rect(screen, playercolors[Color], playerColorbottom)
               # player name
               name.get_bounding_rect()
               pygame.draw.ellipse(screen, 'white', name_rect)
               pygame.draw.ellipse(screen, "black", name_rect, 5)
               screen.blit((name), (name_rect.x + 10, name_rect.y + 10))

               pygame.draw.line(screen, 'black', (name_rect.right + 50, height - 100), (name_rect.right + 50, height),
                                6)
               pygame.draw.line(screen, 'black', (width - 150, height - 100), (width - 150, height), 6)
               screen.blit(player[Color],(name_rect.right+70,height-50))

               if (Quizz):
                    if firstQuest:
                         Response = ClientSocket.recv(1020)
                         quest = Response.decode('utf-8')
                         Questfont = pygame.font.Font(None, 80)
                         Quest = Questfont.render(quest, False, 'black')

                         Quest_rect = Quest.get_rect(center=(width / 2, (height - 100) / 2))
                         firstQuest = False

                    screen.blit(quizzSur, quizzSur_rect)
                    screen.blit(Quest, Quest_rect)
                    answerUser = base_font.render(answer, False, 'black')
                    answerUser_rect = answerUser.get_rect(midbottom=(width / 2, height - 20))
                    screen.blit(answerUser, answerUser_rect)
                    display_time()
                    # if  int((pygame.time.get_ticks() / 1000)-starttime)>int(max_time):
                    #      if answer=="":
                    #           answer="-1000000"
                    #      ClientSocket.send(str.encode(answer))
                    #      waitAnswer = True
                    #
                    #      Quizz = False
                    #      answer = ""
               if winGame:
                    screen.blit(background,(0,0))
                    screen.blit(WinText,WinText_rect)
                    screen.blit(QuitTex,QuitTex_rect)
               if loseGame:
                    screen.blit(background,(0,0))
                    screen.blit(LoseText,LoseText_rect)
                    screen.blit(QuitTex, QuitTex_rect)




          elif nickName:

               screen.blit(Background,(0,0))
               screen.blit(Register, Register_rect)

               if(wait==True):

                    screen.blit(RegisterS, RegisterS_rect)

                    ClientSocket.setblocking(False)
                    try:
                         race_len = ClientSocket.recv(1020)
                         Race_Len = int(race_len)
                         ClientSocket.send(str.encode("Ready"))
                         firstQuest=True
                         wait=False
                         ClientSocket.setblocking(True)
                         nickName = False
                         gameActive = True
                         Quizz = True




                    except:
                         pass



               if(InvalidChar==True):
                    screen.blit(Invalidchartext,Invalidchartext_rect)
               if(NickNameExisted==True):
                    screen.blit(NameExistText,NameExistText_rect)



               text_surface = base_font.render(user_text, True, 'black')
               pygame.draw.rect(screen, 'white', input_rect)
               pygame.draw.rect(screen, 'black', input_rect, 6)
               screen.blit(text_surface, (input_rect.x + 10, input_rect.y + 5))


          pygame.display.update()
          clock.tick(60)




     ClientSocket.close()

if __name__ == '__main__':

     if len(sys.argv) == 2:
          port = int(sys.argv[1])
          Game_Client(port=port)
     else:
          Game_Client()