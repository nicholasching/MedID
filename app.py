from flask import Flask, Response, render_template
import cv2
import time

app = Flask(__name__)

# Initialize OpenCV (replace with your video source)
video_source = cv2.VideoCapture(0)  # Use 0 for default camera, or a path to video file

# Check if video source is open
if not video_source.isOpened():
    print("Error: Could not open video source.")
    exit()

def generate_frames():
    while True:
        success, frame = video_source.read()
        if not success:
            break
        # Optionnal: Process frame if needed here
        # Convert frame to JPEG format
        _, buffer = cv2.imencode('.jpg', frame) 
        # Yield the JPEG image in bytes
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def home():
    return render_template('index.html')


# @app.route('/')
# def index():
#     return """
#     <html>
#     <head>
#         <title>Live Video Stream</title>
#     </head>
#     <body>
#         <h1>Live Video Stream</h1>
#         <img src="/video_feed" id="video_stream">
#     </body>
#     </html>
#     """


if __name__ == '__main__':
    app.run(debug=True)