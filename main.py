





import cv2
import pyautogui
from hand_tracking import HandTracker

pyautogui.FAILSAFE = False

cap = cv2.VideoCapture(0)
tracker = HandTracker()

click_delay = 0
gesture_frames = 0
prev_status = None

cv2.namedWindow("AirInput - Gesture Mode", cv2.WINDOW_NORMAL)
cv2.resizeWindow("AirInput - Gesture Mode", 1280, 720)


def finger_status(lm_list, hand_label):

    status = []

    if not lm_list:
        return [0,0,0,0,0]

    # Thumb
    if hand_label == "Right":
        status.append(1 if lm_list[4][1] > lm_list[3][1] else 0)
    else:
        status.append(1 if lm_list[4][1] < lm_list[3][1] else 0)

    fingers = [(8,6),(12,10),(16,14),(20,18)]

    for tip,pip in fingers:
        if lm_list[tip][2] < lm_list[pip][2] - 15:
            status.append(1)
        else:
            status.append(0)

    return status


def perform_gesture(status):

    key = tuple(status)

    actions = {

        # INDEX -> VOLUME UP
        (0,1,0,0,0): ("Volume Up",
        lambda: pyautogui.press("volumeup")),

        # LITTLE -> VOLUME DOWN
        (0,0,0,0,1): ("Volume Down",
        lambda: pyautogui.press("volumedown")),

        # THUMB -> MUTE / UNMUTE
        (1,0,0,0,0): ("Mute/Unmute",
        lambda: pyautogui.press("volumemute")),

        # INDEX + MIDDLE -> SCROLL UP
        (0,1,1,0,0): ("Scroll Up",
        lambda: pyautogui.scroll(400)),

        # RING + LITTLE -> SCROLL DOWN
        (0,0,0,1,1): ("Scroll Down",
        lambda: pyautogui.scroll(-400)),

    }

    if key in actions:

        name, func = actions[key]

        try:
            func()
        except:
            pass

        return name

    return None


while True:

    success, img = cap.read()
    if not success:
        break

    img = cv2.flip(img,1)

    img = tracker.find_hands(img)
    lm_list, hand_label = tracker.get_positions(img)

    gesture_name = None

    if len(lm_list) != 0:

        status = finger_status(lm_list, hand_label)

        # EXIT GESTURE (OPEN PALM)
        if status == [1,1,1,1,1]:

            cv2.putText(img,"EXITING TO MENU",
            (400,200),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,(0,0,255),3)

            cv2.imshow("AirInput - Gesture Mode",img)
            cv2.waitKey(500)
            break


        if status == prev_status:
            gesture_frames += 1
        else:
            gesture_frames = 1

        prev_status = status


        if click_delay == 0 and gesture_frames > 10:

            gesture_name = perform_gesture(status)
            click_delay = 25


        cv2.putText(img,f"{status}",
        (20,50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,(255,0,0),3)


        if gesture_name:

            cv2.putText(img,f"Action: {gesture_name}",
            (20,100),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,(0,255,0),3)


    if click_delay > 0:
        click_delay -= 1


    cv2.imshow("AirInput - Gesture Mode",img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()