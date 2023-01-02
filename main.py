import face_recognition
import cv2
import numpy as np
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mess
import tkinter.simpledialog as tsd
from PIL import Image,ImageTk
import cv2,os
import csv
import numpy as np
import pandas as pd
import datetime
import time
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo


global name
name=""
# This is a demo of running face recognition on live video from your webcam. It's a little more complicated than the
# other example, but it includes some basic performance tweaks to make things run a lot faster:
#   1. Process each video frame at 1/4 resolution (though still display it at full resolution)
#   2. Only detect faces in every other frame of video.

# PLEASE NOTE: This example requires OpenCV (the `cv2` library) to be installed only to read from your webcam.
# OpenCV is *not* required to use the face_recognition library. It's only required if you want to run this
# specific demo. If you have trouble installing it, try any of the other demos that don't require it instead.

# Get a reference to webcam #0 (the default one)



def main1():
    message1 = tk.Label(frame1, text="Searching..." ,bg="green yellow" ,fg="black"  ,width=15 ,height=1, activebackground = "yellow" ,font=('times', 15, ' bold '))
    message1.place(x=140, y=380)  
    video_capture = cv2.VideoCapture('{}'.format(filename1))
    # Load a sample picture and learn how to recognize it.
    criminal_image = face_recognition.load_image_file('{}'.format(filename))
    criminal_face_encoding = face_recognition.face_encodings(criminal_image)[0]
    if len(criminal_face_encoding)>0:
        pass
    else:
        message1.configure(text="Not Detected") 

    # Create arrays of known face encodings and their names
    known_face_encodings = [criminal_face_encoding]
    known_face_names = ["Criminal"]

    # Initialize some variables
    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True

    while True:
        # Grab a single frame of video
        ret, frame = video_capture.read()

        # Only process every other frame of video to save time
        if process_this_frame:
            # Resize frame of video to 1/4 size for faster face recognition processing
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = small_frame[:, :, ::-1]
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame,4)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = ""

                # # If a match was found in known_face_encodings, just use the first one.
                # if True in matches:
                #     first_match_index = matches.index(True)
                #     name = known_face_names[first_match_index]

                # Or instead, use the known face with the smallest distance to the new face
                
                
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]
                    

                face_names.append(name)

        process_this_frame = not process_this_frame


        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left+10, top+10), (right+10, bottom+30), (0, 0, 255), 2)
            # Draw a label with a name below the face
            cv2.rectangle(frame, (left+10, bottom +30), (right+10, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom +20), font, 0.5, (255, 255, 255), 1)
        
            if name!="":
                if cv2.imwrite("frame.jpg", frame):
                     image3 =Image.open("frame.jpg")
                     resized_image3= image3.resize((440,280), Image.ANTIALIAS)
                     test1 = ImageTk.PhotoImage(resized_image3)
                     label3 = tk.Label(window,image=test1,width=440,height=280,bg="#262523")
                     label3.image = test1
                     label3.place(x=720,y=190)
                     message1.configure(text="Criminal Dected!!!")
                     video_capture.release()
                     cv2.destroyAllWindows()
                     break
    
        cv2.imshow('Video', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break        
                      
    video_capture.release()
    cv2.destroyAllWindows()   
           

        
 



def select_file():
    filetypes = (
        ('jpg', '*.jpg'),
        ('All files', '*.*'),
        ('png', '*.png'),('jpeg', '*.jpeg')
    )
    global filename
    filename = fd.askopenfilename(
        title='Open a file',
        initialdir='/',
        filetypes=filetypes)
    criminal()

def select_file1():
    filetypes = (
        ('mp4', '*.mp4'),
        ('All files', '*.*'),
    )
    global filename1
    filename1 = fd.askopenfilename(
        title='Open a file',
        initialdir='/',
        filetypes=filetypes) 
    main1()




###############################GUI#######################################################
    
global key
key = ''

ts = time.time()
date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
day,month,year=date.split("-")

mont={'01':'January',
      '02':'February',
      '03':'March',
      '04':'April',
      '05':'May',
      '06':'June',
      '07':'July',
      '08':'August',
      '09':'September',
      '10':'October',
      '11':'November',
      '12':'December'
      }


######################################## GUI FRONT-END ###########################################

window = tk.Tk()
window.geometry("1280x720")
window.resizable(True,False)
window.title("Criminal Identification system")
window.configure(background='#262523')
frame1 = tk.Frame(window,highlightthickness=2, bg="#262523")
frame1.place(relx=0.55, rely=0.17, relwidth=0.38, relheight=0.70)

frame2 = tk.Frame(window,highlightthickness=2, bg="#262523")
frame2.place(relx=0.10, rely=0.17, relwidth=0.34, relheight=0.70)


message3 = tk.Label(window, text="Criminal Identification System" ,fg="white",bg="#262523" ,width=55 ,height=1,font=('times', 29, ' bold '))
message3.place(x=10, y=10)

frame3 = tk.Frame(window, bg="#c4c6ce")
frame3.place(relx=0.46, rely=0.09, relwidth=0.22, relheight=0.07)

frame4 = tk.Frame(window, bg="#c4c6ce")
frame4.place(relx=0.30, rely=0.09, relwidth=0.2, relheight=0.07)


datef = tk.Label(frame4, text = day+"-"+mont[month]+"-"+year+"", fg="green yellow",bg="#262523" ,width=55 ,height=1,font=('times', 20, ' bold '))
datef.pack(fill='both',expand=1)

clock = tk.Label(frame3,fg="green yellow",bg="#262523" ,width=55 ,height=1,font=('times', 22, ' bold '))
clock.pack(fill='both',expand=1)


head2 = tk.Label(frame2, text="       CRIMINAL'S IMAGE      ", fg="black",bg="lime green" ,font=('times', 17, ' bold ') )
head2.grid(row=0,column=1)
head2.place(x=60,y=10)
head3 = tk.Label(frame2, text="   SELECT THE FOOTAGE  ", fg="black",bg="lime green" ,font=('times', 17, ' bold ') )
head3.place(x=60,y=350)



head1 = tk.Label(frame1, text="       DETECTION     ", fg="black",bg="lime green" ,font=('times', 17, ' bold ') )
head1.place(x=140,y=10)



  



def criminal():
    image11 = Image.open(str(filename))
    resized_image = image11.resize((150,150), Image.ANTIALIAS)
    test = ImageTk.PhotoImage(resized_image)
    label1 = tk.Label(window,image=test,width=150,height=150)
    label1.image = test
    label1.place(x=256,y=280)


image1 = Image. open("img.png")
resized_image= image1.resize((100,100), Image.ANTIALIAS)
image2 =  ImageTk. PhotoImage(resized_image)
image_label = tk.Label(window , image =image2,bg="#262523")
image_label.place(x = 160, y = 5)






###################### BUTTONS ##################################



quitWindow = tk.Button(frame1, text="QUIT", command=window.destroy  ,fg="black"  ,bg="green yellow"  ,width=10 ,height=1, activebackground = "white" ,font=('times', 15, ' bold '))
quitWindow.place(x=180, y=450)


select= tk.Button(frame2, text="Select file", command=select_file  ,fg="black"  ,bg="green yellow"  ,width=10 ,height=1, activebackground = "white" ,font=('times', 12, ' bold '))
select.place(x=150, y=100)

select2= tk.Button(frame2, text="Select file", command=select_file1 ,fg="black"  ,bg="green yellow"  ,width=10 ,height=1, activebackground = "white" ,font=('times', 12, ' bold '))
select2.place(x=150, y=400)


##################### END ######################################


window.mainloop()






