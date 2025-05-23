import sqlite3

class Student:
    def __init__(self, first_name, last_name, middle_name, group, grades):
        self.first_name = first_name
        self.last_name = last_name
        self.middle_name = middle_name
        self.group = group
        self.grades = grades

con = sqlite3.connect('students.db')
cursor = con.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        middle_name TEXT NOT NULL,
        group_name TEXT NOT NULL,
        grades TEXT NOT NULL
    )
""")
con.commit()

def add_student(student):
    grades_str = ','.join(map(str, student.grades))
    cursor.execute('''
                INSERT INTO students (first_name, last_name, middle_name, group_name, grades)
                VALUES (?, ?, ?, ?, ?)
            ''', (student.first_name, student.last_name, student.middle_name, student.group, grades_str))
    con.commit()

def get_all_students():
    cursor.execute('SELECT * FROM students')
    return cursor.fetchall()

def get_student(student_id):
    cursor.execute('SELECT * FROM students WHERE id = ?', (student_id,))
    student_information = cursor.fetchone()
    grades = list(map(int, student_information[5].split(',')))
    return f"id: {student_information[0]}\nИмя: {student_information[1]}\nФамилия: {student_information[2]}\nОтчество: {student_information[3]}\nГруппа: {student_information[4]}\nОценки: {grades}\nСредний балл: {sum(grades) / len(grades)}"

def update_student(student_id, student):
    grades_str = ','.join(map(str, student.grades))
    cursor.execute('''
                UPDATE students
                SET first_name = ?, last_name = ?, middle_name = ?, group_name = ?, grades = ?
                WHERE id = ?
            ''', (student.first_name, student.last_name, student.middle_name, student.group, grades_str, student_id))
    con.commit()

def delete_student(student_id):
    cursor.execute('DELETE FROM students WHERE id = ?', (student_id,))
    con.commit()

def get_average_grade_group(group_name):
    cursor.execute('SELECT grades FROM students WHERE group_name = ?', (group_name,))
    students_grades = cursor.fetchall()
    all_grades = [int(grade) for student in students_grades for grade in student[0].split(',')]
    return sum(all_grades) / len(all_grades)

while True:
    choice = int(input("1 - Добавление нового студента\n2 - Просмотр всех студентов\n3 - Просмотр одного студента, включая его средний балл\n4 - Редактирование студента\n5 - Удаление студента\n6 - Просмотр среднего балла студентов у конкретной группы\n7 - Завершить\nДействие: "))
    if choice == 1:
        first_name = input("Введите имя: ")
        last_name = input("Введите фамилию: ")
        middle_name = input("Введите отчество: ")
        group = input("Введите группу: ")
        grades_input = input("Введите оценки через запятую (5,5,5,5): ")
        grades = list(map(int, grades_input.split(',')))
        student = Student(first_name, last_name, middle_name, group, grades)
        add_student(student)
        print("Студент создан")

    elif choice == 2:
        all_students = get_all_students()
        print("Список студентов:")
        for i in all_students:
            print(f"ID: {i[0]}, Имя: {i[1]}, Фамилия: {i[2]}, Отчество: {i[3]}, Группа: {i[4]}")

    elif choice == 3:
        all_students = get_all_students()
        for i in all_students:
            print(f"ID: {i[0]}, Имя: {i[1]}, Фамилия: {i[2]}, Группа: {i[4]}")
        student_id = int(input("Введите ID студента: "))
        print(get_student(student_id))

    elif choice == 4:
        all_students = get_all_students()
        for i in all_students:
            print(f"ID: {i[0]}, Имя: {i[1]}, Фамилия: {i[2]}, Группа: {i[4]}")
        student_id = int(input("Введите ID студента, которого хотите отредактировать: "))
        print(get_student(student_id))
        print("Введите новые данные для студента:")
        first_name = input("Введите имя: ")
        last_name = input("Введите фамилию: ")
        middle_name = input("Введите отчество: ")
        group = input("Введите группу: ")
        grades_input = input("Введите оценки через запятую (5,5,5,5): ")
        grades = list(map(int, grades_input.split(',')))
        updated_student = Student(first_name, last_name, middle_name, group, grades)
        update_student(student_id, updated_student)
        print(get_student(student_id))

    elif choice == 5:
        all_students = get_all_students()
        for i in all_students:
            print(f"ID: {i[0]}, Имя: {i[1]}, Фамилия: {i[2]}, Группа: {i[4]}")
        student_id = int(input("Введите ID студента, которого хотите удалить: "))
        delete_student(student_id)
        print("Студент удалён")

    elif choice == 6:
        group_name = input("Введите номер группы: ")
        print(f"Средний балл всей группы: {get_average_grade_group(group_name)}")

    elif choice == 7:
        break