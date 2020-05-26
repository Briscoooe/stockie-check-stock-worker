import mysql.connector
import settings

conn = None

def connect():
    global conn
    print('Connecting to DB...')
    conn = mysql.connector.connect(
        host=settings.DB_HOST,
        user=settings.DB_USER,
        passwd=settings.DB_PASSWORD,
        database=settings.DB_NAME
    )
    print('Done')

def run_select(query, values = ()):
    print('Running query', query, values)
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query, values)
    rows = cursor.fetchall()
    cursor.close()
    return rows

def run_update(query, values = ()):
    print('Running query', query, values)
    try:
        cursor = conn.cursor(prepared=True)
        print(cursor)
        cursor.execute(query, values)
    except mysql.connector.errors.OperationalError as err:
        print('in err')
        print(err)
    else:
        conn.commit()
        cursor.close()
