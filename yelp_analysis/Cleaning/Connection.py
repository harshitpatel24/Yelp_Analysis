import MySQLdb

def get_connection():
    try:
        conn=MySQLdb.connect(db='project2',user='root',passwd='harshit24')
        return conn
    except:
        print("Database Connection Failed.....")
        return

def trim_categories():
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("select distinct(category) from business_category")
        categories = cur.fetchall()
        for category in categories:
            print("Updating", category[0])
            new_category = category[0].strip()
            cur.execute('update business_category set category = "{0}" where category = "{1}"'.format(new_category, category[0]))
            conn.commit()
    except:
        print('Failed to execute....')

trim_categories()