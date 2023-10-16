import sqlite3
import getpass
import datetime

# Connect to database (it creates a new database if it doesn't exist)
con = sqlite3.connect('users.db')


cur = con.cursor()


# Create table
cur.execute('''CREATE TABLE IF NOT EXISTS users
               (username text PRIMARY KEY, password text)''')

cur.execute('''CREATE TABLE IF NOT EXISTS notes
                (id INTEGER PRIMARY KEY AUTOINCREMENT, date text, subject text, note_text text, www text,
                username text, FOREIGN KEY(username) REFERENCES users(username))''')

def create_note(userName):
    """### This function creates a note and adds it to the list of notes
    #### Parameters:
        userName (str): The username of the user creating the note
    #### Returns:
            None"""

    user = userName
    print("User: " + user)
    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("Date: " + date)
    subject = input("Please enter the subject: ")
    subject = subject.upper()
    note_text = input("Please enter the note text: ")
    web = ""
    web = input("Please enter a web URL (you can leave it in blank):")

    # Insert new note
    try:
        cur.execute("INSERT INTO notes (date, subject, note_text, www, username) VALUES (?, ?, ?, ?, ?)", (date, subject, note_text, web, user))
        con.commit()
        print("Note created successfully")
    except sqlite3.Error as e:
        print("Error creating note: ", e)


def create_user():

    print("Please enter a username and password to register")
    username = input("Username: ")
    password = getpass.getpass("Password: ")
    # Insert new user
    try:
        cur.execute("INSERT INTO users VALUES (?, ?)", (username, password))
        con.commit()
        print("User created successfully")
    except sqlite3.IntegrityError:
        print("Username already exists please try again")
        create_user()


def login():
    """### This function logs in a user
    #### Parameters:
        None
    #### Returns:
            None"""

    username = input("Username: ")
    password = getpass.getpass("Password: ")
    # Check if user exists and password is correct
    res = cur.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = res.fetchone()
    if user:
        print("Welcome, " + user[0])
        return user[0]
    else:
        print("Invalid username or password")
        return None


def main():
    global UserName
    print("Welcome to the note taking app")
    print("1. Login")
    print("2. Register")
    print("3. Exit")
    userInput = input("Please select an option: ")
    if userInput == "1":
        UserName = login()
    elif userInput == "2":
        create_user()
    elif userInput == "3":
        print("Exiting...")
        exit()
    try:
        logged_in = True
        while logged_in:
            print("1. Create a note")
            print("2. Retrieve a note")
            print("3. Delete a note")
            print("4. Edit a note")
            print("5. Logout")

            user_input = input("Please select an option:")
            if user_input == "1":
                create_note(UserName)
            elif user_input == "2":
                cur.execute("SELECT * FROM notes")
                rows = cur.fetchall()
                for row in rows:
                    print(row)

                #show_notes(userName=userName)
                pass
            elif user_input == "3":
                #delete_note_by_subject(userName)
                pass
            elif user_input == "4":
                #edit_note(userName)
                pass
            elif user_input == "5":
                print("Logging out")
                logged_in = False
            else:
                print("Invalid option")
    except KeyboardInterrupt:
        print("")
        print("")
        print("Exiting...")
        print("")
        exit()


while True:
    main()
