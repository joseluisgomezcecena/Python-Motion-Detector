import os
import glob
import cv2
import time  # for delay
from emailsender import send_email  # for sending email when motion is detected.
from threading import Thread  # for sending email asynchronously.

video = cv2.VideoCapture(0)  # 0 for webcam, 1 for external camera.
time.sleep(1)  # 1 second delay

first_frame = None
status_list = []  # to store the status of the object.
count = 1  # to store the number of saved files.


def clean_folder():
    print("Cleaning folder...")
    images = glob.glob('images/*.png')
    for image in images:
        os.remove(image)
    print("Folder cleaned.")


while True:
    status = 0  # no motion detected.
    check, frame = video.read()

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # converting to gray scale.
    gray_frame_blur = cv2.GaussianBlur(gray_frame, (21, 21), 0)  # blurring the image.

    if first_frame is None:
        first_frame = gray_frame_blur

    # getting the difference between the first frame and the current frame.
    delta_frame = cv2.absdiff(first_frame, gray_frame_blur)

    # setting the threshold for the difference between the first frame and the current frame.
    # if the difference is greater than 30, then it will be shown as white.
    # if the difference is less than 30, then it will be shown as black.
    thresh_frame = cv2.threshold(delta_frame, 60, 255, cv2.THRESH_BINARY)[1]
    dil_frame = cv2.dilate(thresh_frame, None, iterations=2)
    cv2.imshow("Detecting Movement...", dil_frame)

    contours, check = cv2.findContours(dil_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        if cv2.contourArea(contour) < 8000:
            continue
        (x, y, w, h) = cv2.boundingRect(contour)
        rectangle = cv2.rectangle(frame, (x,y), (x+w, y+h), (0, 255, 0), 3)

        # sending email when motion is detected.
        if rectangle.any():
            status = 1  # motion detected.
            cv2.imwrite(f"images/image-{count}.jpg", frame)  # saving the captured frame.
            count = count + 1  # incrementing the count.

            all_images = glob.glob("images/*.png")  # getting all the saved images.

            if len(all_images) > 0:
                index = int(len(all_images)/2)  # getting the index of the last saved image.
                image_with_object = all_images[index]  # getting the last saved image.
            else:
                image_with_object = "images/image-1.jpg"

    status_list.append(status)
    status_list = status_list[-2:]

    if status_list[0] == 1 and status_list[1] == 0:
        # sending email asynchronously.
        email_thread = Thread(target=send_email, args=(image_with_object, ))  # creating a thread.
        email_thread.daemon = True  # making the thread daemon.

        clean_folder_thread = Thread(target=clean_folder)  # creating a thread.
        clean_folder_thread.daemon = True  # making the thread daemon.

        email_thread.start()  # starting the thread.


        #send_email(image_with_object)
        #clean_folder()  # cleaning the folder after sending the email.

    print(status_list)

    cv2.imshow("Detecting Movement ...", frame)
    key = cv2.waitKey(1)

    if key == ord('q'):
        break

video.release()
clean_folder_thread.start()  # starting the thread.
#yrepuapenhbscxvn
