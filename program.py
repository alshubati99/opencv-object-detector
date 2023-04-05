import cv2
# import numpy as np # to create buttoms
from gui_buttons import Buttons
# initialize Buttons:
button = Buttons()
button.add_button("person",20,20)
button.add_button("cell phone",20,100)
# opencv DNN
net = cv2.dnn.readNet("dnn_model/yolov4-tiny.weights", "dnn_model/yolov4-tiny.cfg")
model = cv2.dnn_DetectionModel(net)
model.setInputParams(size = (320, 320), scale = 1/255)

# Load classes' lists:
classes = []
with open("dnn_model/classes.txt","r") as file_object:
    for class_name in file_object.readlines():
       # print(class_name)
       class_name = class_name.strip()
       classes.append(class_name)
print("Objects lists:")
print(classes)

# Initialize camera
cap = cv2.VideoCapture(0)
# improve the resolution
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1288)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
# Full HD 1920 x 1000
button_person = False
def click_button(event,x,y,flags,params):
    global button_person
    if event ==cv2.EVENT_LBUTTONDOWN:
        button.button_click(x,y)
        # polygon = np.array([[(20,20),(228,20),(220,70),(20,70)]])
        # is_inside = cv2.pointPolygonTest(polygon,(x,y),False)
        # if is_inside>0:
        #     print("We're clicking inside button",x,y)
        #     if button_person is False:
        #         button_person = True
        #     else:
        #         button_person = False
        #     print("now button person is :", button_person)
cv2.namedWindow("Frame") #must have same name with name
cv2.setMouseCallback("Frame",click_button)
while True:
    # get frames:
    ret, frame = cap.read()
    # get active buttons list:
    active_buttons = button.active_buttons_list()
    print(active_buttons)
    # ***Object Detection***: 
    (class_ids, scores, bboxes)= model.detect(frame) # bbox = bounding boxes. where the object is located
    # score = how confident is the algorithm about the detection
    for class_id,score,bbox in zip(class_ids,scores,bboxes):
        (x,y,w,h) = bbox
        class_name = classes[class_id]
        
        # if class_name == "person" and button_person is True:
        if class_name in active_buttons:
        # The rectangle
            cv2.rectangle(frame,(x,y),(x+w,y+h),(200,0,50), 3)
            # import classes from classes.txt:
            cv2.putText(frame,class_name,(x,y-10),cv2.FONT_HERSHEY_PLAIN,2,(200,0,50),2)

    # Display Buttons: 
    button.display_buttons(frame)

    # # Create Button: 
    # cv2.rectangle(frame, (20,20),(250,70),(0,0.200),-1) 
    # polygon = np.array([[(20,20),(228,20),(220,70),(20,70)]])
    # cv2.fillPoly(frame,polygon,(0,0,200))
    # cv2.putText(frame,"Person",(30,68),cv2.FONT_HERSHEY_PLAIN,3,(255,255,255),3)

    # print("class ids", class_ids)
    # print("score",scores)
    # print("bboxes",bboxes)

    cv2.imshow("Frame",frame)
    key = cv2.waitKey(1) # to close the window
    if key == 27:
        break
cap.release()
cv2.destroyAllWindows()
