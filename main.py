import cv2
import mediapipe as mp
import time
import math as m
import easygui


# colors
red = (0, 0, 255)
blue = (255, 0, 0)
magenta = (255, 0, 255)
cyan = (255, 255, 0)
yellow = (0, 255, 255)
purple = (128, 0, 128)
green = (0, 255, 0)
black = (0, 0, 0)
white = (255, 255, 255)
draw_color = blue

# thickness
th1 = 3
th2 = 5
th3 = 8
th4 = 12
th5 = 17
thickness = th1

# checks if dot is inside the circle
def inside(x, y, center, r):
    if(m.sqrt((x-center[0])**2+(y-center[1])**2) < r): return True
    else: return False

cap = cv2.VideoCapture(0) # camera object
canvas = cv2.imread('canvas.jpg') # drawing canvas
canvas_height, canvas_width, channels = canvas.shape # canvas parameters

edge_thickness = 5 #rectangle edge thickness

cache = canvas.copy()
clear_canvas = canvas.copy()

mpHands = mp.solutions.hands # MediaPipe solution object
hands = mpHands.Hands(max_num_hands = 1) # hand object
mpDraw = mp.solutions.drawing_utils # drawing on hand

# fps
pTime = 0
cTime = 0

cont = 0 # currently drawing

# previous finger coordinates
px = 0
py = 0

scale=2

infloop = 1

while infloop:
    # draws color rectangles
    cv2.rectangle(canvas, (0, 0), (int(canvas_width/10), int(canvas_height/6)), blue, cv2.FILLED)
    cv2.rectangle(canvas, (0, 0), (int(canvas_width/10), int(canvas_height/6)), black, thickness= edge_thickness)
    cv2.rectangle(canvas, (0, int(canvas_height/6)), (int(canvas_width/10), 2*int(canvas_height/6)), red, cv2.FILLED)
    cv2.rectangle(canvas, (0, int(canvas_height/6)), (int(canvas_width/10), 2*int(canvas_height/6)), black, thickness= edge_thickness)
    cv2.rectangle(canvas, (0, int(2*canvas_height/6)), (int(canvas_width/10), 3*int(canvas_height/6)), magenta, cv2.FILLED)
    cv2.rectangle(canvas, (0, int(2*canvas_height/6)), (int(canvas_width/10), 3*int(canvas_height/6)), black, thickness= edge_thickness)
    cv2.rectangle(canvas, (0, int(3*canvas_height/6)), (int(canvas_width/10), 4*int(canvas_height/6)), cyan, cv2.FILLED)
    cv2.rectangle(canvas, (0, int(3*canvas_height/6)), (int(canvas_width/10), 4*int(canvas_height/6)), black, thickness= edge_thickness)
    cv2.rectangle(canvas, (0, int(4*canvas_height/6)), (int(canvas_width/10), 5*int(canvas_height/6)), yellow, cv2.FILLED)
    cv2.rectangle(canvas, (0, int(4*canvas_height/6)), (int(canvas_width/10), 5*int(canvas_height/6)), black, thickness= edge_thickness)
    cv2.rectangle(canvas, (0, int(5*canvas_height/6)), (int(canvas_width/10), canvas_height), white, cv2.FILLED) # rubber
    cv2.rectangle(canvas, (0, int(5*canvas_height/6)), (int(canvas_width/10), canvas_height), black, thickness= edge_thickness)

    # brush thickness circles
    cv2.circle(canvas, (int(canvas_width/8), int(canvas_height/10)), scale*th1, black, cv2.FILLED)
    cv2.circle(canvas, (int(2*canvas_width/8), int(canvas_height/10)), scale*th2, black, cv2.FILLED)
    cv2.circle(canvas, (int(3*canvas_width/8), int(canvas_height/10)), scale*th3, black, cv2.FILLED)
    cv2.circle(canvas, (int(4*canvas_width/8), int(canvas_height/10)), scale*th4, black, cv2.FILLED)
    cv2.circle(canvas, (int(5*canvas_width/8), int(canvas_height/10)), scale*th5, black, cv2.FILLED)

    # clear canvas button
    cv2.rectangle(canvas, (canvas_width-490, 100), (canvas_width-125, 220), black, 5)
    cv2.putText(canvas, "CLEAR", (canvas_width-490+25, 220-30), cv2.FONT_HERSHEY_COMPLEX, 3, black, 3)

    # save button
    cv2.rectangle(canvas, (canvas_width-490, 250), (canvas_width-125, 370), black, 5)
    cv2.putText(canvas, "SAVE", (canvas_width-490+60, 370-30), cv2.FONT_HERSHEY_COMPLEX, 3, black, 3)

    # exit button
    cv2.rectangle(canvas, (canvas_width-490, 390), (canvas_width-125, 510), black, 5)
    cv2.putText(canvas, "EXIT", (canvas_width-490+80, 510-30), cv2.FONT_HERSHEY_COMPLEX, 3, black, 3)

    success, img = cap.read() # reads image from camera
    h, w, c = img.shape # image dimensions
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # BGR to RGB
    results = hands.process(imgRGB) # searching for a hand

    if results.multi_hand_landmarks: # if the hand is found
        for handLms in results.multi_hand_landmarks: # for each hand
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
            index_lm_x = handLms.landmark[8].x # relative index finger x coordinate
            index_lm_y = handLms.landmark[8].y # relative index finger y coordinate
            middle_lm_x = handLms.landmark[12].x # relative middle finger x coordinate
            middle_lm_y = handLms.landmark[12].y # relative middle finger y coordinate

            # drawing color
            if canvas_width*(1-index_lm_x) < int(canvas_width/10):
                if canvas_height*index_lm_y < int(canvas_height/6): draw_color = blue
                elif canvas_height*index_lm_y < int(2*canvas_height/6): draw_color = red
                elif canvas_height*index_lm_y < int(3*canvas_height/6): draw_color = magenta
                elif canvas_height*index_lm_y < int(4*canvas_height/6): draw_color = cyan
                elif canvas_height*index_lm_y < int(5*canvas_height/6): draw_color = yellow
                elif canvas_height*index_lm_y < int(canvas_height):     draw_color = white # rubber

            # line thickness
            if inside(canvas_width*(1-index_lm_x), canvas_height*index_lm_y, (int(canvas_width/8), int(canvas_height/10)), 5*th1): thickness = th1
            if inside(canvas_width*(1-index_lm_x), canvas_height*index_lm_y, (int(2*canvas_width/8), int(canvas_height/10)), 5*th2): thickness = th2
            if inside(canvas_width*(1-index_lm_x), canvas_height*index_lm_y, (int(3*canvas_width/8), int(canvas_height/10)), 5*th3): thickness = th3
            if inside(canvas_width*(1-index_lm_x), canvas_height*index_lm_y, (int(4*canvas_width/8), int(canvas_height/10)), 5*th3): thickness = th4
            if inside(canvas_width*(1-index_lm_x), canvas_height*index_lm_y, (int(5*canvas_width/8), int(canvas_height/10)), 5*th3): thickness = th5

            # clear canvas
            if canvas_width*(1-index_lm_x) < canvas_width-125 and canvas_width*(1-index_lm_x) > canvas_width-490:
                if canvas_height*index_lm_y < 220 and canvas_height*index_lm_y > 100:
                    canvas = clear_canvas.copy() # deep copy of the canvas
                    cache = clear_canvas.copy()

            # save canvas
            if canvas_width*(1-index_lm_x) < canvas_width-125 and canvas_width*(1-index_lm_x) > canvas_width-490:
                if canvas_height*index_lm_y < 370 and canvas_height*index_lm_y > 250:
                    img_name = easygui.filesavebox(msg='Choose the name of your image', title='Save Image', default='HandDrawingImage', filetypes=['*.jpg'])
                    if img_name:
                        img_name = img_name + '.jpg'
                        cv2.imwrite(img_name, canvas)

            # exit
            if canvas_width*(1-index_lm_x) < canvas_width-125 and canvas_width*(1-index_lm_x) > canvas_width-490:
                if canvas_height*index_lm_y < 510 and canvas_height*index_lm_y > 390:
                    infloop = 0

            x8, y8 = int(index_lm_x*w), int(index_lm_y*h) # index finger coordinates [px]
            x12, y12 = int(middle_lm_x*w), int(middle_lm_y*h) # middle finger coordinates [px]
            cv2.circle(img, (x12, y12), 10, (0, 0, 255), 5, cv2.FILLED)
            cv2.circle(img, (x8, y8), 10, (255, 0, 0), 5, cv2.FILLED)
            if m.sqrt((x8 - x12)**2 + (y8-y12)**2)>45: # if fingers are part
                if cont == 0:
                    canvas = cache.copy() # deep copy
                    cv2.circle(canvas, (int(canvas_width*(1-index_lm_x)), int(canvas_height*index_lm_y)), thickness, draw_color, cv2.FILLED)
                    cont = 1
                else:
                    cv2.line(canvas, (px, py), (int(canvas_width*(1-index_lm_x)), int(canvas_height*index_lm_y)), draw_color, thickness)
                px = int(canvas_width*(1-index_lm_x))
                py = int(canvas_height*index_lm_y)
            else:
                if (cont == 1): 
                    cache = canvas.copy()
                cont = 0
                cv2.putText(canvas, str("PAUSED"), (canvas_width-500, 70), cv2.FONT_HERSHEY_COMPLEX, 3, red, 3)
                cv2.circle(canvas, (int(canvas_width*(1-handLms.landmark[8].x)), int(canvas_height*handLms.landmark[8].y)), 2, green, cv2.FILLED)
    else: cont == 0       
    img = cv2.flip(img,1)
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime=cTime
    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_COMPLEX, 3, (255, 0, 0), 3)

    canvas[canvas_height-h:, canvas_width-w:] = img # adding camera image to canvas

    cv2.imshow("Drawing", canvas)
    cv2.waitKey(1)

cv2.destroyAllWindows()