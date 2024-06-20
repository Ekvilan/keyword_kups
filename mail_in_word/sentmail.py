import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def send_word_email(file_path, username, password, sender_emails):
    # Создание объекта сообщения
    msg = MIMEMultipart()
    msg["From"] = username
    # Correct: Join email addresses into a single string
    msg["To"] = ", ".join(sender_emails) 

    # Добавление файла Word
    attachment = MIMEBase("application", "octet-stream")
    with open(file_path, "rb") as file:
        attachment.set_payload(file.read())
    encoders.encode_base64(attachment)
    attachment.add_header(
        "Content-Disposition",
        f"attachment; filename={file_path.split('/')[-1]}",
    )
    msg.attach(attachment)

    # Отправка сообщения
    with smtplib.SMTP_SSL("smtp.mail.ru", 465) as server:  # Используйте "smtp.mail.ru" для mail.ru
        server.login(username, password)
        server.sendmail(username, sender_emails, msg.as_string())


