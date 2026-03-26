import csv
from connect import get_connection

# CSV-дан контактілерді қосу
def add_contacts_from_csv(filename):
    conn = get_connection()
    cur = conn.cursor()
    with open(filename, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            cur.execute(
                "INSERT INTO contacts (first_name, last_name, phone, email) VALUES (%s,%s,%s,%s)",
                (row['first_name'], row['last_name'], row['phone'], row['email'])
            )
    conn.commit()
    cur.close()
    conn.close()
    print("Contacts added from CSV!")

# Консольден контакт қосу
def add_contact():
    first = input("First name: ")
    last = input("Last name: ")
    phone = input("Phone: ")
    email = input("Email: ")

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO contacts (first_name, last_name, phone, email) VALUES (%s,%s,%s,%s)",
        (first, last, phone, email)
    )
    conn.commit()
    cur.close()
    conn.close()
    print("Contact added!")

# CSV-дан алғашқы контактілерді қосу
add_contacts_from_csv("contacts.csv")

# Консольден жаңа контакт қосу
add_contact()
