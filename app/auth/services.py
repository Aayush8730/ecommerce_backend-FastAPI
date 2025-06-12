import smtplib
from email.message import EmailMessage
from app.core.logging import logger

def send_reset_email(email: str, token: str):
    reset_link = f"http://localhost:8000/auth/reset-password-form?token={token}"
    msg = EmailMessage()
    msg['Subject'] = "Reset Your Password"
    msg['From'] = "aayushp0822@gmail.com"
    msg['To'] = email
    msg.set_content(f"Click the link to reset your password: {reset_link}")
    logger.info(f"password reset email sent to {email}")
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls()
        smtp.login("aayushp0822@gmail.com", "qjuxgeygpyhpqtqt")
        smtp.send_message(msg)
