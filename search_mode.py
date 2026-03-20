
















import cv2
import mediapipe as mp
import pyautogui
import subprocess
import time
import math
import sys
import os

# OPEN CHROME
subprocess.Popen(r"C:\Program Files\Google\Chrome\Application\chrome.exe")
time.sleep(5)

# SNAP CHROME RIGHT
pyautogui.hotkey("win","right")

# OPEN GOOGLE
pyautogui.write("google.com")
pyautogui.press("enter")
time.sleep(3)

screen_w, screen_h = pyautogui.size()

# CAMERA
cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)

cv2.namedWindow("AirInput Search",cv2.WINDOW_NORMAL)
cv2.resizeWindow("AirInput Search",1280,720)

mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=1)
mpDraw = mp.solutions.drawing_utils

typed_delay = 0

keys = [
['Q','W','E','R','T','Y','U','I','O','P'],
['A','S','D','F','G','H','J','K','L'],
['Z','X','C','V','B','N','M'],
['SPACE','BACK','SEARCH']
]


# FUNCTION TO RETURN TO MAIN UI
def go_back_menu():
    cap.release()
    cv2.destroyAllWindows()
    subprocess.Popen([sys.executable, "airinput_menu.py"])
    os._exit(0)


def draw_keyboard(img):

    key_w = 60
    key_h = 60
    gap = 8

    start_x = 20
    start_y = 300

    key_locations = []

    for i,row in enumerate(keys):

        x = start_x

        for key in row:

            if key == "SPACE":
                w = key_w * 3
            elif key == "BACK":
                w = key_w * 2
            elif key == "SEARCH":
                w = key_w * 3
            else:
                w = key_w

            y = start_y + i*(key_h + gap)

            cv2.rectangle(img,(x,y),(x+w,y+key_h),(255,0,255),2)

            cv2.putText(img,key,(x+10,y+40),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8,(255,255,255),2)

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

        screen_x = screen_w / 1280 * index_x
        screen_y = screen_h / 720 * index_y
        pyautogui.moveTo(screen_x,screen_y)

        distance = math.hypot(thumb_x-index_x, thumb_y-index_y)

        for key,x,y,w,h in key_locations:

            if x < index_x < x+w and y < index_y < y+h:

                cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),3)

                if distance < 40 and typed_delay == 0:

                    if key == "SPACE":
                        pyautogui.write(" ")

                    elif key == "BACK":
                        go_back_menu()

                    elif key == "SEARCH":
                        pyautogui.press("enter")

                    else:
                        pyautogui.write(key)

                    typed_delay = 15

        if distance < 30 and typed_delay == 0:
            pyautogui.click()
            typed_delay = 15

    if typed_delay > 0:
        typed_delay -= 1

    cv2.putText(img,"AIRINPUT CHROME SEARCH",
                (20,50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,(0,255,0),3)

    cv2.imshow("AirInput Search",img)

    if cv2.waitKey(1) & 0xFF == 27:
        go_back_menu()