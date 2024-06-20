import imaplib
import email
from email.header import decode_header
import os

def mail_in_word(username, password, sender_emails):
# Данные для входа

    # Подключение к серверу
    mail = imaplib.IMAP4_SSL('imap.mail.ru')
    mail.login(username, password)

    # Выбор почтового ящика
    mail.select('inbox')

    # Поиск непрочитанных писем
    status, messages = mail.search(None, '(OR {} UNSEEN)'.format(' '.join(f'(FROM "{email}")' for email in sender_emails)))
    if status == 'OK':
        # Преобразование строки ответа в список идентификаторов сообщений
        messages = messages[0].split()

        for mail_id in messages:
            # Получение данных письма
            status, data = mail.fetch(mail_id, '(RFC822)')
            if status == 'OK':
                # Парсинг данных письма
                msg = email.message_from_bytes(data[0][1])
                # Обход всех частей письма
                for part in msg.walk():
                    # Поиск вложений
                    if part.get_content_maintype() == 'multipart' or part.get('Content-Disposition') is None:
                        continue
                    # Получение имени файла
                    filename = part.get_filename()
                    if filename:
                        filename = decode_header(filename)[0][0]
                        if isinstance(filename, bytes):
                            # Декодирование имени файла
                            filename = filename.decode('KOI8-R')
                        # Сохранение файла
                        filepath = os.path.join('D:\\create_program\\mail_in_word', filename)
                        with open(filepath, 'wb') as f:
                            f.write(part.get_payload(decode=True))
                # Отметить письмо как прочитанное
                mail.store(mail_id, '+FLAGS', '\\Seen')

    # Закрытие соединения
    mail.close()
    mail.logout()
    return filepath