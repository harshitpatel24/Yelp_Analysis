import mysql.connector

def get_connection():
    try:
        conn= mysql.connector.connect(db='project2',user='root',passwd='harshit24')
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


def get_all_business_count():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("CALL get_distinct_businesses_count(@data)")
    cur.execute("select @data")
    return cur.fetchone()[0]


def get_all_category_count():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("CALL get_distinct_category_count(@data)")
    cur.execute("select @data")
    return cur.fetchone()[0]

def get_top_10_categories():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("CALL get_top_10_categories_demo()")
    top_10_categories = []
    for category in cur.fetchall():
        top_10_categories.append(category[0])
    return top_10_categories

def get_filtered_users(min_review_count):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("CALL get_filtered_users("+str(min_review_count)+")")
    filtered_users = []
    for user in cur.fetchall():
        filtered_users.append(user[0])
    return filtered_users


def get_filtered_reviews(star, category):
    conn = get_connection()
    cur = conn.cursor()
    print(category)
    cur.execute("CALL get_filtered_reviews "+str(tuple((str(star), category))))
    filtered_reviews = []
    for review in cur.fetchall():
        filtered_reviews.append([review[0], review[1]])
    return filtered_reviews


def get_filtered_businesses(category):
    filtered_businesses = dict()
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("CALL get_filtered_businesses('{0}')".format(category))
    for business in cur.fetchall():
        filtered_businesses[business[0]] = business[1]
    return filtered_businesses


def get_columns(db_name, table_name):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("CALL get_columns('{0}','{1}')".format(db_name, table_name))
    columns = []
    for column in cur.fetchall():
        columns.append(column[0])
    return columns

def get_data(table_name):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("CALL get_data('{0}')".format(table_name))
    #columns = []
    #for column in cur.fetchall():
    #    columns.append(column[0])
    return cur.fetchall()


def get_review_distribution():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("CALL get_review_distribution()")
    stars = []
    count = []

    for column in cur.fetchall():
        stars.append(column[0])
        count.append(column[1])
    return stars,count

def get_businesses_with_highest_ratings(count):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("CALL get_businesses_with_highest_ratings("+str(count)+")")
    businesses = []
    reviews = []

    for column in cur.fetchall():
        businesses.append(column[0])
        reviews.append(column[1])
    return businesses, reviews


def get_business_categories_with_highest_ratings(count):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("CALL get_business_categories_with_highest_ratings("+str(count)+")")
    categories = []
    reviews = []

    for column in cur.fetchall():
        categories.append(column[0])
        reviews.append(column[1])
    return categories, reviews


def get_businesses_five_stars(count):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("CALL get_businesses_five_stars(" + str(count) + ")")
    businesses = []
    reviews = []

    for column in cur.fetchall():
        businesses.append(column[0])
        reviews.append(column[1])
    return businesses, reviews
#print(get_review_distribution())