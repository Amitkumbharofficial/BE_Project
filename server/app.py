from flask import Flask, request, send_file
import cv2
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  


UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
car_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_car.xml')


@app.route('/process-video', methods=['POST'])
def process_video():
    file = request.files['video']  
    video_path = os.path.join(UPLOAD_FOLDER, file.filename)
    
    file.save(video_path)
    
    cap = cv2.VideoCapture(video_path)
    
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    output_path = os.path.join(UPLOAD_FOLDER, 'processed_' + file.filename)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    print(f"Output video path: {output_path}, codec: {fourcc}, fps: {fps}, size: {(width, height)}")

    # if os.path.exists(output_path):
    #     print("Processed video written successfully.")
    # else:
    #     print("Error writing the processed video.")


    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("End of video or error in reading frames.")
            break
        
        print("Processing frame...")  # Add this to see if frames are being processed

        
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        
        faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        
        
        for (x, y, w, h) in faces:
            # Draw a rectangle around the face
            # cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            roi = frame[y:y+h, x:x+w]
        
            # Apply Gaussian blur to the ROI
            blurred_roi = cv2.GaussianBlur(roi, (99, 99), 30)
        
            # Replace the original ROI with the blurred version
            frame[y:y+h, x:x+w] = blurred_roi
        
            # Draw a blue rectangle around the face (optional)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        
        out.write(frame)
    
    cap.release()
    out.release()
    
    return send_file(output_path, mimetype='video/mp4')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
