import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from mail_in_word.mail import mail_in_word
from mail_in_word.table import find_paragraf
from queries.core import insert_data
# логин и пароль
username = 'uvpo.sakh.pso@mail.ru'
password = 'e9vxZhxDq5seN1A3g1Nt'
# откуда получаем файлы
sender_emails = ['a.shmatkov@sakhalin.gov.ru']
sender_email= ['a.reukov@sakhalin.gov.ru']
# сsender_emailsкачиваем файлы
folderpath = mail_in_word(username, password, sender_emails)
# получаmем готового файла
kupt_list = find_paragraf(folderpath)
insert_data(kupt_list)
