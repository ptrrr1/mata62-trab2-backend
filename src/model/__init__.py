from model.manager import DBManager

dbmanager = DBManager()

if dbmanager.test_conn():
    dbmanager.create_tables()
