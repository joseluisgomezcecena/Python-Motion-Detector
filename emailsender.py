import smtplib
import imghdr
from email.message import EmailMessage

PASSWORD = "yrepuapenhbscxvn"
SENDER_EMAIL = "joseluisgomezcecegna@gmail.com"
RECEIVER_EMAIL = "joseluisgomezcecegna@gmail.com"

def send_email(image_path):
    print("Sending email...")
    email_message = EmailMessage()
    email_message["Subject"] = "Motion Detected!"
    email_message.set_content("Motion Detected! Please check the attachment.")

    with open(image_path, "rb") as image_file:
        content = image_file.read()
    email_message.add_attachment(content, maintype="image", subtype=imghdr.what(None, content), filename=image_path)

    gmail = smtplib.SMTP("smtp.gmail.com", 587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(SENDER_EMAIL, PASSWORD)
    gmail.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, email_message.as_string())
    gmail.quit()

    print("Email Sent!")

if __name__ == "__main__":
    send_email(image_path="images/image-1.jpg")
