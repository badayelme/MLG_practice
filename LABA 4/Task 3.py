import sqlite3
import psutil
from datetime import datetime

def create_database():
    con = sqlite3.connect('system_monitor.db')
    cursor = con.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS system_monitor (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            time TEXT,
            cpu REAL,
            memory REAL,
            disk REAL
        )
    ''')
    con.commit()

def monitor_system():
    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent
    time = datetime.now().strftime("%H:%M:%S")
    con = sqlite3.connect('system_monitor.db')
    cursor = con.cursor()
    cursor.execute('''
            INSERT INTO system_monitor (time, cpu, memory, disk)
            VALUES (?, ?, ?, ?)
        ''', (time, cpu, memory, disk))
    con.commit()
    print(f"CPU: {cpu}%, Memory: {memory}%, Disk: {disk}%")

def view_data():
    con = sqlite3.connect('system_monitor.db')
    cursor = con.cursor()
    cursor.execute('SELECT * FROM system_monitor')
    monitor = cursor.fetchall()
    for i in monitor:
        print(f"ID: {i[0]}, Time: {i[1]}, CPU: {i[2]}, Memory: {i[3]}, Disk: {i[4]}")

create_database()

while True:
    choice = int(input("1 - Monitor\n2 - View\n3 - Exit\nДействие: "))
    if choice == 1:
        monitor_system()
    elif choice == 2:
        view_data()
    elif choice == 3:
        break