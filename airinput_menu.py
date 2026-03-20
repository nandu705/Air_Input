import cv2
import mediapipe as mp
import math
import subprocess
import sys

def start_menu():

    cap = cv2.VideoCapture(0)
    cap.set(3,1280)
    cap.set(4,720)

    mpHands = mp.solutions.hands
    hands = mpHands.Hands(max_num_hands=1)
    mpDraw = mp.solutions.drawing_utils

    delay = 0

    def draw_buttons(img):

        buttons = [
            ("MOUSE",150,200,220,80),
            ("KEYBOARD",450,200,260,80),
            ("SEARCH",800,200,220,80),
            ("QUIT",550,400,200,80)
        ]

        for name,x,y,w,h in buttons:

            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,255),3)

            cv2.putText(img,name,(x+20,y+50),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,(255,255,255),3)

        return buttons


    while True:

        success,img = cap.read()
        if not success:
            break

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

        buttons = draw_buttons(img)

        if len(lmList) != 0:

            ix,iy = lmList[8]   # index finger
            tx,ty = lmList[4]   # thumb

            cv2.circle(img,(ix,iy),10,(0,255,0),cv2.FILLED)

            distance = math.hypot(tx-ix,ty-iy)

            for name,x,y,w,h in buttons:

                if x < ix < x+w and y < iy < y+h:

                    cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),4)

                    if distance < 40 and delay == 0:

                        cap.release()
                        cv2.destroyAllWindows()

                        if name == "MOUSE":
                            subprocess.run([sys.executable,"main.py"])

                        elif name == "KEYBOARD":
                            subprocess.run([sys.executable,"keyboard_mode.py"])

                        elif name == "SEARCH":
                            subprocess.run([sys.executable,"search_mode.py"])

                        elif name == "QUIT":
                            exit()

                        # reopen menu after mode closes
                        cap = cv2.VideoCapture(0)
                        cap.set(3,1280)
                        cap.set(4,720)

                        delay = 20

        if delay > 0:
            delay -= 1

        cv2.putText(img,"AIRINPUT MAIN MENU",
                    (420,100),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1.2,(0,255,0),3)

        cv2.imshow("AirInput Menu",img)

        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()


start_menu()