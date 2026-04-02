from connect import get_connection

def search_contacts(pattern):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM get_contacts_by_pattern(%s);", (pattern,))
    for row in cur.fetchall():
        print(row)
    cur.close()
    conn.close()

def upsert_contact(name, phone):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("CALL upsert_contact(%s, %s);", (name, phone))
    conn.commit()
    cur.close()
    conn.close()

def bulk_insert(names, phones):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("CALL bulk_insert_contacts(%s, %s);", (names, phones))
    conn.commit()
    cur.close()
    conn.close()

def delete_contact(value):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("CALL delete_contact(%s);", (value,))
    conn.commit()
    cur.close()
    conn.close()
