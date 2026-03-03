import sqlite3

def init_db():
    con = sqlite3.connect("jarvis.db")
    cursor = con.cursor()
    
    # sys_command table
    cursor.execute('''CREATE TABLE IF NOT EXISTS sys_command (
                        id INTEGER PRIMARY KEY AUTOINCREMENT, 
                        name VARCHAR(100), 
                        path VARCHAR(1000))''')
    
    # web_command table
    cursor.execute('''CREATE TABLE IF NOT EXISTS web_command (
                        id INTEGER PRIMARY KEY AUTOINCREMENT, 
                        name VARCHAR(100), 
                        url VARCHAR(1000))''')
    
    # contacts table
    # Based on features.py: InsertContacts(Name, MobileNo, Email, City) -> (None, Name, MobileNo, Email, City)
    cursor.execute('''CREATE TABLE IF NOT EXISTS contacts (
                        id INTEGER PRIMARY KEY AUTOINCREMENT, 
                        name VARCHAR(200), 
                        mobile_no VARCHAR(255), 
                        email VARCHAR(255), 
                        city VARCHAR(255))''')
    
    # info table
    cursor.execute('''CREATE TABLE IF NOT EXISTS info (
                        name VARCHAR(100), 
                        designation VARCHAR(50), 
                        mobileno VARCHAR(40), 
                        email VARCHAR(200), 
                        city VARCHAR(300))''')
    
    # Insert some default values if tables are empty
    cursor.execute("SELECT COUNT(*) FROM sys_command")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO sys_command (name, path) VALUES (?, ?)", ('notepad', 'C:\\Windows\\System32\\notepad.exe'))
        cursor.execute("INSERT INTO sys_command (name, path) VALUES (?, ?)", ('calculator', 'C:\\Windows\\System32\\calc.exe'))
    
    cursor.execute("SELECT COUNT(*) FROM web_command")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO web_command (name, url) VALUES (?, ?)", ('google', 'https://www.google.com'))
        cursor.execute("INSERT INTO web_command (name, url) VALUES (?, ?)", ('youtube', 'https://www.youtube.com'))
    
    con.commit()
    con.close()
    print("Database initialized successfully.")

if __name__ == "__main__":
    init_db()
