import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from mail_in_word.connection import export_to_word
from queries.core import select_dataBase
data = select_dataBase()
falename = export_to_word(data)
send_word_email(falename, username, password, sender_email)
print("файл отправлен")
