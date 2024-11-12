import cv2 as cv
import time 
import random
import mediapipe as mp
import math
import numpy as np

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles=mp.solutions.drawing_styles
mp_hands= mp.solutions.hands

hands= mp_hands.Hands(static_image_mode=False,max_num_hands=1,min_detection_confidence=0.7,min_tracking_confidence=0.5)

curr_Frame =0 
prev_Frame=0
delta_Time=0

next_Time_to_Spawn= 0
Speed=[0,5]
F_size= 30
S_rate=1
Score =0
Lives =10
Diff_level=1
game_over=False

slash= np.array([[]],np.int32)
slash_color=(255,255,255)
slash_length= 19

w=h=0
Fruits=[]

def Spawn_fruits():
    fruit={}
    random_x= random.randint(15,600)
    random_color= (random.randint(0,255),random.randint(0,255),random.randint(0,255))
    fruit["Color"] = random_color                                                       
    fruit["Curr_position"]=[random_x,440]
    fruit["Next_position"] = [0,0]
    Fruits.append(fruit)

def Fruit_Movement(Fruits , speed):
    global Lives

    for fruit in Fruits:
        if (fruit["Curr_position"][1]) < 20 or (fruit["Curr_position"][0]) > 650 :
            Lives = Lives - 1
           
            Fruits.remove(fruit)

        cv.circle(img,tuple(fruit["Curr_position"]),F_size,fruit["Color"],-1)
        fruit["Next_position"][0]= fruit["Curr_position"][0] + speed[0] 
        fruit["Next_position"][1]= fruit["Curr_position"][1] - speed[1] 

        fruit["Curr_position"]=fruit["Next_position"]

def distance(a , b):
    x1 = a[0]
    y1 = a[1]

    x2 = b[0]
    y2 = b[1]

    d =math.sqrt(pow(x1 -x2,2)+pow(y1-y2,2))
    return int(d)
cap = cv.VideoCapture(0)           
while(cap.isOpened()):              
    success , img = cap.read()     
    if not success:
        print("skipping frame")
        continue
    h, w, c = img.shape             
    
    img = cv.cvtColor(cv.flip(img, 1), cv.COLOR_BGR2RGB)  
    results = hands.process(img)    
    img = cv.cvtColor(img, cv.COLOR_RGB2BGR)     
    if results.multi_hand_landmarks:                          
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(                        
                img,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style())

            
            for id , lm in enumerate(hand_landmarks.landmark): 
                if id == 8:                                       
                    index_pos=(int(lm.x * w) ,int(lm.y * h))      
                                                                  
                                                                  
                    cv.circle(img,index_pos,18,slash_color,-1)   
                    
                    slash=np.append(slash,index_pos)              

                    while len(slash) >= slash_length:             
                        slash = np.delete(slash , len(slash) -slash_length , 0)

                    for fruit in Fruits:                              
                        d= distance(index_pos,fruit["Curr_position"])           
                        cv.putText(img,str(d),fruit["Curr_position"],cv.FONT_HERSHEY_SIMPLEX,2,(0,0,0),2,3)
                        if(d < F_size):                                     
                            Score= Score + 100                               
                            slash_Color = fruit["Color"]                        
                            Fruits.remove(fruit)                                

           
  
        if Score % 1000 ==0 and Score != 0:        
            Diff_level = (Score / 1000) + 1    
            Diff_level= int(Diff_level)  
            print(Diff_level)
            Spawn_Rate =  Diff_level * 4/5     
            Speed[0] = Speed[0] * Diff_level   
            Speed[1] = int(5 * Diff_level /2) 
            print(Speed)

    if(Lives<=0): 
        game_over=True

    slash=slash.reshape((-1,1,2))                    
    cv.polylines(img,[slash],False,slash_color,15,0) 

    curr_Frame = time.time()
    delta_Time = curr_Frame - prev_Frame
    FPS = int(1/delta_Time)                 
    cv.putText(img,"FPS : " +str(FPS),(int(w*0.82),50),cv.FONT_HERSHEY_TRIPLEX,0.6,(18,24,181),2)                 
    cv.putText(img,"Score: "+str(Score),(int(w*0.35),90),cv.FONT_HERSHEY_TRIPLEX,1,(187,212,61),3)                
    cv.putText(img,"Level: "+str(Diff_level),(int(w*0.01),90),cv.FONT_HERSHEY_TRIPLEX,1,(187,212,61),3)    
    cv.putText(img,"Lives remaining : " + str(Lives), (200, 50), cv.FONT_HERSHEY_TRIPLEX, 0.8, (187,212,61), 2)  


    prev_Frame = curr_Frame

    
    if not (game_over):                               
        if  (time.time() > next_Time_to_Spawn):       
            Spawn_fruits()
            next_Time_to_Spawn = time.time() + (1 / S_rate)

        Fruit_Movement(Fruits,Speed)


    else:                                     # if game is over then print it and clear all the fruits
        cv.putText(img, "GAME OVER", (int(w * 0.1), int(h * 0.6)), cv.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 255), 3)
        Fruits.clear()
        
    cv.imshow("img", img)                    

    if cv.waitKey(5) & 0xFF == ord("q"):
        break     

cap.release()                                 
cv.destroyAllWindows()





