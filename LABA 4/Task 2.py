import sqlite3

def create_tables():
    con = sqlite3.connect('i_love_drink.db')
    cursor = con.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Drinks (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        drink_strength REAL,
        quantity INTEGER,
        price REAL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Ingredients (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        quantity INTEGER
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Composition (
        drink_id INTEGER,
        ingredient_id INTEGER,
        quantity INTEGER,
        FOREIGN KEY (drink_id) REFERENCES Drinks(id),
        FOREIGN KEY (ingredient_id) REFERENCES Ingredients(id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Operations (
        id INTEGER PRIMARY KEY,
        type TEXT NOT NULL,
        drink_id INTEGER,
        quantity INTEGER,
        date DATETIME,
        FOREIGN KEY (drink_id) REFERENCES Drinks(id)
    )
    ''')

    con.commit()

def add_drink(name, drink_strength, quantity, price):
    con = sqlite3.connect('i_love_drink.db')
    cursor = con.cursor()
    cursor.execute('''
    INSERT INTO Drinks (name, drink_strength, quantity, price)
    VALUES (?, ?, ?, ?)
    ''', (name, drink_strength, quantity, price))
    con.commit()

def add_ingredient(name, quantity):
    con = sqlite3.connect('i_love_drink.db')
    cursor = con.cursor()
    cursor.execute('''
    INSERT INTO Ingredients (name, quantity)
    VALUES (?, ?)
    ''', (name, quantity))
    con.commit()

def add_drink_composition(drink_id, ingredient_id, quantity):
    con = sqlite3.connect('i_love_drink.db')
    cursor = con.cursor()
    cursor.execute('''
    INSERT INTO Composition (drink_id, ingredient_id, quantity)
    VALUES (?, ?, ?)
    ''', (drink_id, ingredient_id, quantity))
    con.commit()

def sell_drink(drink_id, quantity):
    con = sqlite3.connect('i_love_drink.db')
    cursor = con.cursor()

    cursor.execute('''
    UPDATE Drinks SET quantity = quantity - ? WHERE id = ?
    ''', (quantity, drink_id))

    cursor.execute('''
    INSERT INTO Operations (type, drink_id, quantity, date)
    VALUES (?, ?, ?, CURRENT_TIMESTAMP)
    ''', ('Sale', drink_id, quantity))
    con.commit()

def restock_drink(item, drink_id, quantity):
    con = sqlite3.connect('i_love_drink.db')
    cursor = con.cursor()

    if item == 1:
        cursor.execute('''
        UPDATE Drinks SET quantity = quantity + ? WHERE id = ?
        ''', (quantity, drink_id))
    elif item == 2:
        cursor.execute('''
        UPDATE Ingredients SET quantity = quantity + ? WHERE id = ?
        ''', (quantity, drink_id))

    cursor.execute('''
    INSERT INTO Operations (type, drink_id, quantity, date)
    VALUES (?, ?, ?, CURRENT_TIMESTAMP)
    ''', ('Restock', drink_id, quantity))
    con.commit()

def drinks_info():
    con = sqlite3.connect('i_love_drink.db')
    cursor = con.cursor()
    cursor.execute('SELECT id, name, drink_strength, quantity, price FROM Drinks')
    drinks = cursor.fetchall()
    for i in drinks:
        print(f"ID: {i[0]}, Название: {i[1]}, Крепость напитка: {i[2]}%, Количество: {i[3]}, Цена: {i[4]}руб")

def ingredients_info():
    con = sqlite3.connect('i_love_drink.db')
    cursor = con.cursor()
    cursor.execute('SELECT id, name, quantity FROM Ingredients')
    ingredients = cursor.fetchall()
    for i in ingredients:
        print(f"ID: {i[0]}, Название: {i[1]}, Количество: {i[2]}")

def info_drink_composition(drink_id):
    con = sqlite3.connect('i_love_drink.db')
    cursor = con.cursor()

    cursor.execute('''
        SELECT Ingredients.name, Composition.quantity
        FROM Composition, Ingredients
        WHERE Composition.ingredient_id = Ingredients.id
        AND drink_id = ?
        ''', (drink_id,))

    composition = cursor.fetchall()

    print(f"\nСостав напитка: {drink_id}")
    for i in composition:
        print(f"Ингредиент: {i[0]}, Количество: {i[1]}")

create_tables()

while True:
    choice = int(input("1 - Добавить напиток\n2 - Добавить ингредиент\n3 - Добавить ингредиент в напиток\n4 - Продать напиток\n5 - Пополнить запас\n6 - Вывести все напитки\n7 - Вывести состав напитка\n8 - Завершить\nДействие: "))

    if choice == 1:
        name = input("Введите название напитка: ")
        drink_strength = float(input("Введите крепость алкоголя: "))
        quantity = int(input("Введите количество: "))
        price = float(input("Введите цену: "))
        add_drink(name, drink_strength, quantity, price)
        print("Напиток добавлен")

    elif choice == 2:
        name = input("Введите название ингредиента: ")
        quantity = int(input("Введите количество: "))
        add_ingredient(name, quantity)
        print("Ингредиент добавлен")

    elif choice == 3:
        drinks_info()
        drink_id = int(input("Введите ID напитка: "))
        ingredients_info()
        ingredient_id = int(input("Введите ID ингредиента: "))
        quantity = int(input("Введите количество: "))
        add_drink_composition(drink_id, ingredient_id, quantity)
        print("Ингредиент добавлен в напиток")

    elif choice == 4:
        drinks_info()
        drink_id = int(input("Введите ID напитка: "))
        quantity = int(input("Введите количество: "))
        sell_drink(drink_id, quantity)
        print("Напиток продан")

    elif choice == 5:
        item = int(input("Введите тип товара (1 - напиток/2 - ингредиент): "))
        if item == 1:
            drinks_info()
        elif item == 2:
            ingredients_info()
        drink_id = int(input("Введите ID товара: "))
        quantity = int(input("Введите количество: "))
        restock_drink(item, drink_id, quantity)
        print("Запасы пополнены")

    elif choice == 6:
        drinks_info()

    elif choice == 7:
        drinks_info()
        drink_id = int(input("Введите ID напитка: "))
        info_drink_composition(drink_id)

    elif choice == 8:
        break

    else:
        print("Error!")