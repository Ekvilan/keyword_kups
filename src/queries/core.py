from datetime import timedelta, date
from sqlalchemy import text, select, update, exists
from database import sync_engin, async_engin, Base, session_factory, sessionmaker
from models import metadata_obj, WorkersOrm
today = date.today()

async def get_123_async():
    async with async_engin.connect() as conn:
        res =await conn.execute(text("SELECT 1,2,3 union select 4,5,6;"))
        print(f"{res.first()=}")

def get_123_sync():
    with sync_engin.connect() as conn:
        res = conn.execute(text("SELECT 1,2,3 union select 4,5,6;"))
        print(f"{res.first()=}")

def create_table():
    try:
        sync_engin.echo = True
        Base.metadata.drop_all(sync_engin)
        Base.metadata.create_all(sync_engin)
    except Exception as e:
        print(f"Ошибка при создании таблиц: {e}")
    finally:
        sync_engin.echo = False
def insert_data(kusp_list):
    # Создайте таблицу, если она еще не существует
    create_table()

    with sync_engin.connect() as conn:
        for kusp_dict in kusp_list: # Iterate over the list of dictionaries
            for cups, value in kusp_dict.items():
                # Check if the combination already 
                if not conn.execute(
                    select(
                    exists().where(
                        WorkersOrm.cups == cups,
                        WorkersOrm.value == value
                    )
                )).scalar():
                    new_worker = WorkersOrm(cups=cups, value=value, create_add=date.today())
                    conn.execute(
                        WorkersOrm.__table__.insert(),
                        {"cups": cups, "value": value, "create_add": date.today()} 
                    )
        conn.commit() # Сохраните изменения

@staticmethod
def select_dataBase(chunk_size=5):

    one_week_ago = date.today() - timedelta(days=7)
    
    with session_factory() as session:
        # Выполняем запрос на выборку
        query = (
            select(WorkersOrm.id, WorkersOrm.cups, WorkersOrm.value)
            .where(WorkersOrm.create_add >= one_week_ago)
        )

        # Получаем Cursor и данные по частям
        cursor = session.execute(query)  # Получаем Cursor
        while True:
            chunk = cursor.fetchmany(chunk_size)
            if not chunk:
                break
            yield chunk