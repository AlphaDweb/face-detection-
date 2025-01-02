
# Face Recognition and Email Alert System

This repository implements a **Face Recognition and Email Alert System** using **Flask**, **OpenCV**, and **face_recognition**. The system allows users to upload an image or PDF containing a face, detects faces via a webcam, and sends an email alert when a match is found.

---

## Features

### 1. **Face Recognition**
- Compares uploaded images with live webcam footage to detect matching faces.
- Supports image formats (PNG, JPG, JPEG, GIF) and extracts images from PDF files.

### 2. **Email Alert System**
- Sends an email alert with details of the match if a face is detected.
- Uses **SMTP** with TLS encryption for secure email communication.

### 3. **PDF Image Extraction**
- Extracts the first page as an image if the uploaded file is a PDF.

### 4. **User-Friendly Web Interface**
- Built with **Flask** for an easy-to-use web interface.
- Allows uploading files and triggers webcam-based detection directly.

---

## Applications

- **Attendance Management**: Automatically detect and record attendance based on facial recognition.
- **Security Systems**: Monitor and alert security teams if unauthorized persons are detected.
- **Surveillance**: Enhances surveillance systems with automatic face matching.

---

## Technical Stack

- **Flask**: Lightweight web framework for backend development.
- **OpenCV**: For capturing webcam footage and processing images.
- **Face Recognition**: Built on **dlib** for face detection and encoding.
- **Python SMTP Library**: Sends email alerts securely.
- **pdf2image**: Converts PDF files into image formats for processing.

---

## Installation

### 1. Clone the Repository:
```bash
https://github.com/AlphaDweb/face-detection-.git
cd face-recognition-email-alert
```

### 2. Install Dependencies:
```bash
pip install -r requirements.txt
```

**Note:** Create a `requirements.txt` file with the following content:
```
Flask
opencv-python
face-recognition
pdf2image
pillow
```

### 3. Set Up Email Configuration:
Edit the `app.py` file to include your email credentials:
```python
SENDER_EMAIL = "your-email@gmail.com"
SENDER_PASSWORD = "your-app-password"
RECEIVER_EMAIL = "receiver-email@gmail.com"
```

---

## Usage

1. **Run the Flask Application**:
```bash
python app.py
```

2. **Access the Web Interface**:
Open your browser and go to [http://127.0.0.1:5000](http://127.0.0.1:5000)

3. **Upload an Image or PDF**:
- Submit an image or PDF file through the upload form.
- The system will compare faces and display the result.

4. **Receive Email Alerts**:
- If a match is detected, the system will send an email notification with details.

---

## Project Structure

```
face-recognition-email-alert/
├── app.py                 # Main Flask application
├── templates/
│   ├── index.html         # Upload form template
│   ├── result.html        # Result display template
├── uploads/               # Directory for storing uploaded files
├── requirements.txt       # Dependencies
```

---

## Contributing

Contributions are welcome! If you’d like to improve this project, feel free to fork the repository and submit a pull request.

---

## Acknowledgments

- **OpenCV** for webcam integration and image processing.
- **face_recognition** for easy-to-use face detection algorithms.
- **pdf2image** for PDF-to-image conversion.
- **Flask** for providing a lightweight and scalable web framework.
- Special thanks to the open-source community for tools and support.

---
