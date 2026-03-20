





import cv2
import mediapipe as mp
import pyautogui
import subprocess
import time
import math
import sys

# open notepad
subprocess.Popen("notepad.exe")
time.sleep(1)

# move notepad to right side
pyautogui.hotkey("win","right")

# camera
cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)

cv2.namedWindow("AirInput Keyboard",cv2.WINDOW_NORMAL)
cv2.resizeWindow("AirInput Keyboard",1280,720)

mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=1)
mpDraw = mp.solutions.drawing_utils

typed_delay = 0

keys = [
['Q','W','E','R','T','Y','U','I','O','P'],
['A','S','D','F','G','H','J','K','L'],
['Z','X','C','V','B','N','M'],
['SPACE','EXIT']
]

def draw_keyboard(img):

    key_w = 45
    key_h = 45
    gap = 6

    start_x = 20
    start_y = 400

    key_locations = []

    for i,row in enumerate(keys):

        x = start_x

        for key in row:

            if key == "SPACE":
                w = key_w * 4
            elif key == "EXIT":
                w = key_w * 2
            else:
                w = key_w

            y = start_y + i*(key_h + gap)

            cv2.rectangle(img,(x,y),(x+w,y+key_h),(255,0,255),2)

            cv2.putText(img,key,(x+6,y+30),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,(255,255,255),2)

            key_locations.append((key,x,y,w,key_h))

            x = x + w + gap

    return key_locations


while True:

    success,img = cap.read()
    img = cv2.flip(img,1)

    imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    lmList = []

    if results.multi_hand_landmarks:

        for handLms in results.multi_hand_landmarks:

            for id,lm in enumerate(handLms.landmark):

                h,w,c = img.shape
                cx,cy = int(lm.x*w),int(lm.y*h)
                lmList.append((cx,cy))

            mpDraw.draw_landmarks(img,handLms,mpHands.HAND_CONNECTIONS)

    key_locations = draw_keyboard(img)

    if len(lmList) != 0:

        index_x,index_y = lmList[8]
        thumb_x,thumb_y = lmList[4]

        cv2.circle(img,(index_x,index_y),10,(0,255,0),cv2.FILLED)

        distance = math.hypot(thumb_x-index_x, thumb_y-index_y)

        for key,x,y,w,h in key_locations:

            if x < index_x < x+w and y < index_y < y+h:

                cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),3)

                if distance < 40 and typed_delay == 0:

                    if key == "SPACE":
                        pyautogui.write(" ")

                    elif key == "EXIT":

                        # close notepad
                        pyautogui.hotkey("alt","f4")

                        # release camera
                        cap.release()
                        cv2.destroyAllWindows()

                        # open main UI
                        subprocess.Popen(["python","airinput_menu.py"])

                        # close this script
                        sys.exit()

                    else:
                        pyautogui.write(key)

                    typed_delay = 15

    if typed_delay > 0:
        typed_delay -= 1

    cv2.putText(img,"AIRINPUT KEYBOARD MODE",
                (20,50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,(0,255,0),3)

    cv2.imshow("AirInput Keyboard",img)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()