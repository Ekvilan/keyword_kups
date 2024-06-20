from docx import Document
import re
import os
# Рекурсивная функция для извлечения текста из ячеек, включая вложенные таблицы
def extract_text_from_cell(cell, collected_text):
    cell_text = cell.text.strip()
    if cell_text and cell_text not in collected_text:
        collected_text.add(cell_text)
        return cell_text
    return ""

def extract_text_from_table(table, collected_text):
    full_text = ""
    for row in table.rows:
        row_text = []
        for cell in row.cells:
            cell_text = extract_text_from_cell(cell, collected_text)
            row_text.append(cell_text)
            # Обработка вложенных таблиц
            for nested_table in cell.tables:
                full_text += extract_text_from_table(nested_table, collected_text)
        full_text += ' '.join(filter(None, row_text)) + '\n'
    return full_text

def extract_text_from_doc(doc_path):
    doc = Document(doc_path)
    collected_text = set()
    full_text = ""
    for table in doc.tables:
        full_text += extract_text_from_table(table, collected_text)
    return full_text.strip()

def remove_extra_spaces(text):
    # Разделяем текст на слова и снова соединяем, убирая лишние пробелы
    return ' '.join(text.split())

def split_text_into_kusp(text, word_find):
    # Шаблон для поиска КУСП и номера
    kusp_pattern = re.compile(r'((КУСП|КРСП)\s.*?\d+)')
    # Разбиваем текст по шаблону, сохраняя разделители
    parts = re.split(kusp_pattern, text)
    kusp_dict = {}
    current_key = None

    for part in parts:
        # Если часть соответствует шаблону КУСП, обновляем текущий ключ
        if kusp_pattern.match(part):
            current_key = part
        elif current_key and any(word in part for word in word_find):
            # Если нашли ключевое слово в части, добавляем в словарь
            kusp_dict[current_key] = part
    print(kusp_dict)

    return kusp_dict

word_find = ['взрыв', 'бомба', 'террор', 'дискредитация', 'скончался', 'труп', 'наезд', 'сбил', 'сбит', 'горит', 'пожар',
'возгорание', 'убил', 'убийство', 'смерть', 'смертельные', 'массовое', 'дтп с пострадавшим', 'насильственные действия сексуального характера', 'угроза убиства',
'несовершеннолетний', 'малолетний']

def find_paragraf(folderPath):
    parts = folderPath.split('\\')
    folder_name = '\\'.join(parts[:-1])
    kusp_list = []
    for filename in os.listdir(folder_name):  
        if filename.endswith('.docx'):
            doc_path = os.path.join(folder_name, filename)
            table_text = extract_text_from_doc(doc_path)
            # Очищаем текст с помощью функции remove_extra_spaces
            cleaned_text = remove_extra_spaces(table_text)
            kusp_dict = split_text_into_kusp(cleaned_text, word_find)
            kusp_list.append(kusp_dict) 
    return kusp_list
