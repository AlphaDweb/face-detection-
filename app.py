import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, render_template, request, redirect, url_for, flash
import os
import face_recognition
import cv2
from werkzeug.utils import secure_filename
from pdf2image import convert_from_path

app = Flask(__name__)
app.secret_key = "key"
UPLOAD_FOLDER = './uploads'

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Email configuration
SENDER_EMAIL = "@gmail.com"  # Your email address
RECEIVER_EMAIL = "@gmail.com"  # Receiver's email address
SMTP_SERVER = "smtp.gmail.com"  # SMTP server address (e.g., Gmail: smtp.gmail.com)
SMTP_PORT = 587  # Port for sending email (587 for TLS)
SENDER_PASSWORD = "wife gpic eelg sixa"   # Your email password (or app-specific password)

# Function to check if the file has a valid extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Function to extract images from a PDF
def extract_images_from_pdf(pdf_path):
    images = convert_from_path(pdf_path)
    return images

# Function to send an email when a match is found
def send_email(location):
    try:
        # Set up the MIME
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECEIVER_EMAIL
        msg['Subject'] = "Face Match Detected!"

        # Body of the email
        body = f"A match has been found with the uploaded image. Location: {location}"
        msg.attach(MIMEText(body, 'plain'))

        # Set up the server
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()  # Secure the connection
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        
        # Send the email
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
        server.quit()

    except Exception as e:
        print(f"Error sending email: {str(e)}")

# Function to detect faces using the webcam and match with uploaded image
def detect_faces_webcam(uploaded_image_path):
    try:
        # Load the uploaded image and extract its face encoding
        uploaded_image = face_recognition.load_image_file(uploaded_image_path)
        uploaded_encoding = face_recognition.face_encodings(uploaded_image)[0]

        # Initialize the webcam (0 is the default webcam)
        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            return "Could not access the webcam. Please check the camera."

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Convert the frame to RGB (OpenCV uses BGR by default)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Detect faces in the current frame
            face_locations = face_recognition.face_locations(rgb_frame)
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

            # Compare detected faces with the uploaded face encoding
            for encoding in face_encodings:
                matches = face_recognition.compare_faces([uploaded_encoding], encoding)
                if True in matches:
                    cap.release()
                    location = face_locations[0]  # Get the face location
                    send_email(location)  # Send email with face location
                    return f"Match found in webcam! Location: {location}"

            # Display the current frame
            cv2.imshow("Webcam", frame)

            # Exit on pressing 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
        return "No match found in webcam."

    except Exception as e:
        return f"An error occurred: {str(e)}"

@app.route('/')
def home():
    """
    Render the home page with the upload form.
    """
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    """
    Handles file uploads and initiates face detection using the webcam.
    """
    if 'file' not in request.files:
        flash('Please upload an image.')
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        flash('No file selected!')
        return redirect(request.url)

    if not allowed_file(file.filename):
        flash('Only image files are allowed!')
        return redirect(request.url)

    # Save the uploaded file
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    # Check if the file is a PDF and extract the first page as an image
    if filename.endswith('.pdf'):
        images = extract_images_from_pdf(filepath)
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'extracted_image.jpg')
        images[0].save(image_path, 'JPEG')
        filepath = image_path  # Update filepath to the extracted image

    # Detect faces using the webcam and compare with uploaded image
    result = detect_faces_webcam(filepath)
    return render_template('result.html', result=result)

if __name__ == "__main__":
    app.run(debug=True)
