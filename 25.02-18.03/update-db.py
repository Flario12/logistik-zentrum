import sqlite3

DB_FILE = "logistik_zentrum.db"

def Update_DB():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # SQL-Befehle zum Erstellen der Tabellen
    sql_script = '''
        UPDATE 
    '''

if __name__ == "__main__":
    Update_DB()