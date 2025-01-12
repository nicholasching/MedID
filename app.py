from flask import Flask, Response, render_template
from recognition import Recognition
from fileutil import FileUtil
import cv2
import time
import os
import numpy as np
import argparse

app = Flask(__name__)

# Initialize OpenCV (replace with your video source)
video_source = cv2.VideoCapture(0)  # Use 0 for default camera, or a path to video file

# Check if video source is open
if not video_source.isOpened():
    print("Error: Could not open video source.")
    exit()

# Adjustment Tolerances
tolerance = 0.9

# Constructing Gemini Endpoint
gemini = Recognition()
file = FileUtil()
detailSave = None

# construct the argument parse 
parser = argparse.ArgumentParser(
    description='Script to run MobileNet-SSD object detection network ')
parser.add_argument("--video", help="path to video file. If empty, camera's stream will be used")
parser.add_argument("--prototxt", default="MobileNetSSD_deploy.prototxt",
                                  help='Path to text network file: '
                                       'MobileNetSSD_deploy.prototxt for Caffe model or '
                                       )
parser.add_argument("--weights", default="MobileNetSSD_deploy.caffemodel",
                                 help='Path to weights: '
                                      'MobileNetSSD_deploy.caffemodel for Caffe model or '
                                      )
parser.add_argument("--thr", default=0.2, type=float, help="confidence threshold to filter out weak detections")
args = parser.parse_args()

# Labels of Network.
classNames = { 0: 'background',
    1: 'aeroplane', 2: 'bicycle', 3: 'bird', 4: 'boat',
    5: 'bottle', 6: 'bus', 7: 'car', 8: 'cat', 9: 'chair',
    10: 'cow', 11: 'diningtable', 12: 'dog', 13: 'horse',
    14: 'motorbike', 15: 'person', 16: 'pottedplant',
    17: 'sheep', 18: 'sofa', 19: 'train', 20: 'tvmonitor' }

#Load the Caffe model 
net = cv2.dnn.readNetFromCaffe(args.prototxt, args.weights)

def process_frames(frame):
    # Adding Bounding box
    frame_resized = cv2.resize(frame,(300,300)) # resize frame for prediction

    # MobileNet requires fixed dimensions for input image(s)
    # so we have to ensure that it is resized to 300x300 pixels.
    # set a scale factor to image because network the objects has differents size. 
    # We perform a mean subtraction (127.5, 127.5, 127.5) to normalize the input;
    # after executing this command our "blob" now has the shape:
    # (1, 3, 300, 300)
    blob = cv2.dnn.blobFromImage(frame_resized, 0.007843, (300, 300), (127.5, 127.5, 127.5), False)
    #Set to network the input blob 
    net.setInput(blob)
    #Prediction of network
    detections = net.forward()

    #Size of frame resize (300x300)
    cols = frame_resized.shape[1] 
    rows = frame_resized.shape[0]

    #For get the class and location of object detected, 
    # There is a fix index for class, location and confidence
    # value in @detections array .
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2] #Confidence of prediction 
        if confidence > args.thr: # Filter prediction 
            class_id = int(detections[0, 0, i, 1]) # Class label

            # Object location 
            xLeftBottom = int(detections[0, 0, i, 3] * cols) 
            yLeftBottom = int(detections[0, 0, i, 4] * rows)
            xRightTop   = int(detections[0, 0, i, 5] * cols)
            yRightTop   = int(detections[0, 0, i, 6] * rows)
            
            # Factor for scale to original size of frame
            heightFactor = frame.shape[0]/300.0  
            widthFactor = frame.shape[1]/300.0 
            # Scale object detection to frame
            xLeftBottom = int(widthFactor * xLeftBottom) 
            yLeftBottom = int(heightFactor * yLeftBottom)
            xRightTop   = int(widthFactor * xRightTop)
            yRightTop   = int(heightFactor * yRightTop)
            # Draw location of object  
            cv2.rectangle(frame, (xLeftBottom, yLeftBottom), (xRightTop, yRightTop), (0, 255, 0))

            # Print label and confidence of prediction
            if class_id in classNames:
                label = classNames[class_id] + ": " + str(confidence)
                # print(label) #print class and confidence
                if(classNames[class_id] == "person" and confidence > tolerance):
                    cv2.putText(frame, "Person Detected", (25, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.2*heightFactor, (255, 255, 255))
                    croppedFrame = frame[yLeftBottom:yRightTop, xLeftBottom:xRightTop]
                    return croppedFrame

def generate_frames():
    isCapturing = True
    isSaving = True                         # DELETE PAST TEMP WHENEVER ISSAVING IS SET TO TRUE
    try:
        os.remove("temp.jpg")
    except:
        pass
    lastFailTime = time.time()
    while isCapturing:
        success, frame = video_source.read()
        if not success:
            break

        # Processing Frames
        croppedFrame = process_frames(frame)

        if type(croppedFrame) != np.ndarray:
            lastFailTime = time.time()
        else:
            # print((time.time() - lastFailTime))                       # Print time elapsed
            if not (time.time() - lastFailTime) < 1 and isSaving:
                cv2.imwrite("temp.jpg", croppedFrame)
                isSaving = False

        # Convert frame to JPEG format
        _, buffer = cv2.imencode('.jpg', frame) 
        # Yield the JPEG image in bytes
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/await_client/', methods=['POST'])
def await_client():
    gemini.loadImages()
    while True:
        if(os.path.exists("temp.jpg")):
            break
    return ""

@app.route('/fetch_details/', methods=['POST'])
def fetch_details():
    f = open("temp.txt", "w")
    index = file.readLine(gemini.processNew())
    f.write(index)
    f.close()
    if index != "False":
        print("delete")
        gemini.discardNew()
    return index                                       # If returning "False" to BE, then create new profile instead of read

@app.route('/get_details/', methods=['POST'])
def get_details():
    f = open("temp.txt", 'r')
    index = f.read()
    f.close()
    print(index)
    return index

@app.route('/update_details/<newLine>', methods=['POST'])
def update_details(newLine):
    file.updateLine(newLine)
    return ""

@app.route('/new_details/<newLine>', methods=['POST'])
def new_details(newLine):
    file.newLine(newLine)
    file.saveImage(newLine)
    return ""

@app.route('/get_time/', methods=['POST'])
def get_time():
    return str(f'{time.time():.0f}')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/patientinfo')
def patient():
    return render_template('medical-information.html')

if __name__ == '__main__':
    app.run(debug=True)