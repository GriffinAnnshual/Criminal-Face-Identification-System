from datetime import datetime

import cv2
import numpy as np
import colorama,smtplib
import time
import datetime
import os
import glob
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

net = cv2.dnn.readNet('yolov3_training_last (1).weights', 'yolov3_testing.cfg')
from colorama import Fore, Back, Style
colorama.init(autoreset=True)

classes = []
with open("classes.txt", "r") as f:
    classes = f.read().splitlines()

cap = cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_PLAIN
colors = np.random.uniform(0, 255, size=(100, 3))

while True:
    _, img = cap.read()
    height, width, _ = img.shape

    blob = cv2.dnn.blobFromImage(img, 1/255, (416, 416), (0,0,0), swapRB=True, crop=False)
    net.setInput(blob)
    output_layers_names = net.getUnconnectedOutLayersNames()
    layerOutputs = net.forward(output_layers_names)

    boxes = []
    confidences = []
    class_ids = []

    for output in layerOutputs:
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.2:
                center_x = int(detection[0]*width)
                center_y = int(detection[1]*height)
                w = int(detection[2]*width)
                h = int(detection[3]*height)

                x = int(center_x - w/2)
                y = int(center_y - h/2)

                boxes.append([x, y, w, h])
                confidences.append((float(confidence)))
                class_ids.append(class_id)

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.2, 0.4)

    if len(indexes)>0:
        for j in range(1):
            for i in indexes.flatten():
                x, y, w, h = boxes[i]
                label = str(classes[class_ids[i]])
                confidence = str(round(confidences[i],2))
                color = colors[i]
                cv2.rectangle(img, (x,y), (x+w, y+h), color, 2)
                mini = datetime.datetime.now()
                cv2.putText(img,"HR-" + str(mini.hour) + "  MIN-" + str(mini.minute)  + "  SEC-" + str(mini.second)+"  "+ label + " " + confidence, (x, y+20), font,1,(255,255,255), 2)
                print(mini.minute)
                print(mini.hour)
                if((mini.minute==52 and (mini.second==1))or(mini.minute==55 and (mini.second==1))or(mini.minute==54 and (mini.second==1))):
                    cv2.imwrite("BLOG.png",img)
                    sender = "mersalarulmani@gmail.com"
                    password = "leiivkqkkqgfuyuo"
                    reciever = "mersalarulmani@gmail.com"
                    body = f"""
                       GARBAGE FOUND...
                       NEED TO CLEAN...
                         """
                    message=MIMEMultipart()
                    message.attach(MIMEText(body,'plain'))
                    email_bd = """<pre>GO TO LIVE LOCATION: <a href ="http://localhost:63342/garbage%20detection/map.html?_ijt=67evchieend29upkjd43fcdmpc&_ij_reload=RELOAD_ON_SAVE">click here</a>
                    </pre>
                    """
                    link = MIMEText(email_bd, 'html')
                    filename="BLOG.png"
                    attachment=open(filename,'rb')

                    attachment_package=MIMEBase('application','octet-stream')
                    attachment_package.set_payload((attachment).read())
                    encoders.encode_base64(attachment_package)
                    attachment_package.add_header('Content-Disposition', "attachment; filename= "+filename)
                    message.attach(attachment_package)

                    text=message.as_string()

                    server = smtplib.SMTP('smtp.gmail.com', 587)
                    server.starttls()
                    server.login(sender, password)
                    print(Fore.GREEN + "\nAccount successfully verified!")
                    server.sendmail(sender, reciever, text)
                    server.sendmail(sender, reciever, link.as_string())
                    print(Fore.YELLOW + "\nYour email has been successfully sent to", reciever)
                    server.quit()
                    j+=1

    cv2.imshow('Image', img)
    key = cv2.waitKey(1)
    if key==27:
        break

cap.release()
cv2.destroyAllWindows()





