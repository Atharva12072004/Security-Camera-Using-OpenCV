import cv2
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

# Set up your email information
smtp_server = 'your_smtp_server'
smtp_port = 587
sender_email = 'atharvaharane1272004@gmail.com'
sender_password = 'atharvaharane@12072004'
receiver_email = 'sahilgaikwad882@gmail.com'

# Initialize the camera
cap = cv2.VideoCapture(1)  # You can specify the camera index or a file path here

# Initialize the motion detection variables
previous_frame = None
motion_detected = False

# Create a function to send email notifications
def send_notification(image):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = 'Motion Detected'

    body = 'Motion detected in your security camera.'
    msg.attach(MIMEText(body, 'plain'))

    image = cv2.imencode('.jpg', image)[1].tostring()
    image_part = MIMEImage(image)
    msg.attach(image_part)

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
    except Exception as e:
        print(f"Failed to send email notification: {e}")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    if previous_frame is not None:
        frame_diff = cv2.absdiff(previous_frame, gray)
        _, thresh = cv2.threshold(frame_diff, 25, 255, cv2.THRESH_BINARY)

        if cv2.countNonZero(thresh) > 1000:  # Adjust this threshold as needed
            motion_detected = True
        else:
            motion_detected = False

    if motion_detected:
        send_notification(frame)

    previous_frame = gray

    cv2.imshow('Security Camera', frame)
    if cv2.waitKey(1) & 0xFF == 27:  # Press 'Esc' to exit
        break

cap.release()
cv2.destroyAllWindows()
