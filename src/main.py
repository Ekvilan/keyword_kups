import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from mail_in_word.mail import mail_in_word
from mail_in_word.table import find_paragraf
from queries.core import insert_data
# логин и пароль
username = 'ваш логин'
password = 'уникальный пароль'
# откуда получаем файлы
sender_emails = ['список почт от куда вы получаете файлы']
sender_email= ['список почт куда вы отправляете файлы']
# сsender_emailsкачиваем файлы
folderpath = mail_in_word(username, password, sender_emails)
# получаmем готового файла
kupt_list = find_paragraf(folderpath)
insert_data(kupt_list)
