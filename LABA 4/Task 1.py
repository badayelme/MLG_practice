import sqlite3

class Student:
    def __init__(self, first_name, last_name, middle_name, group, grades):
        self.first_name = first_name
        self.last_name = last_name
        self.middle_name = middle_name
        self.group = group
        self.grades = grades

class Database:
    def __init__(self):
        self.con = sqlite3.connect('students.db')
        self.cursor = self.con.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                middle_name TEXT NOT NULL,
                group_name TEXT NOT NULL,
                grades INTEGER NOT NULL
            )
        """)
        self.con.commit()

    def add_student(self, student):
        grades_str = ','.join(map(str, student.grades))
        self.cursor.execute('''
                    INSERT INTO students (first_name, last_name, middle_name, group_name, grades)
                    VALUES (?, ?, ?, ?, ?)
                ''', (student.first_name, student.last_name, student.middle_name, student.group, grades_str))
        self.con.commit()

    def get_all_students(self):
        self.cursor.execute('SELECT * FROM students')
        return self.cursor.fetchall()

    def get_student(self, student_id):
        self.cursor.execute('SELECT * FROM students WHERE id = ?', (student_id,))
        student_information = self.cursor.fetchone()
        grades = list(map(int, student_information[5].split(',')))
        return print(f"id: {student_information[0]}\nИмя: {student_information[1]}\nФамилия: {student_information[2]}\nОтчество: {student_information[3]}\nГруппа: {student_information[4]}\nОценки: {grades}\nСредний балл: {sum(grades) / len(grades)}")

    def update_student(self,student_id,student):
        grades_str = ','.join(map(str, student.grades))
        self.cursor.execute('''
                    UPDATE students
                    SET first_name = ?, last_name = ?, middle_name = ?, group_name = ?, grades = ?
                    WHERE id = ?
                ''', (student.first_name, student.last_name, student.middle_name, student.group, grades_str,
                      student_id))
        self.con.commit()

    def delete_student(self, student_id):
        self.cursor.execute('DELETE FROM students WHERE id = ?', (student_id,))
        self.con.commit()

    def get_average_grade_group(self, group_name):
        self.cursor.execute('SELECT grades FROM students WHERE group_name = ?', (group_name,))
        students_grades = self.cursor.fetchall()
        all_grades = [int(grade) for student in students_grades for grade in student[0].split(',')]
        return sum(all_grades) / len(all_grades)

database = Database()

while True:
    choice = int(input("1 - Добавление нового студента\n2 - Просмотр всех студентов\n3 - Просмотр одного студента, включая его средний балл\n4 - Редактирование студента\n5 - Удаление студента\n6 - Просмотр среднего балла студентов у конкретной группы\n7 - Завершить\nДействие: "))
    if choice == 1:
        first_name = input("Введите имя: ")
        last_name = input("Введите фамилию: ")
        middle_name = input("Введите отчество: ")
        group = input("Введите группу: ")
        grades_input = input("Введите оценки через запятую (5,5,5,5): ")
        grades = list(map(int, grades_input.split(',')))
        student = Student(first_name,last_name,middle_name,group,grades)
        database.add_student(student)
        print("Студент создан")
    elif choice == 2:
        all_students = database.get_all_students()
        print("Список студентов:")
        for i in all_students:
            print(f"ID: {i[0]}, Имя: {i[1]}, Фамилия: {i[2]},Отчество: {i[3]} Группа: {i[4]}")
    elif choice == 3:
        all_students = database.get_all_students()
        for i in all_students:
            print(f"ID: {i[0]}, Имя: {i[1]}, Фамилия: {i[2]}, Группа: {i[4]}")
        student_id = int(input("Введите ID студента: "))
        student_info = database.get_student(student_id)
    elif choice == 4:
        all_students = database.get_all_students()
        for i in all_students:
            print(f"ID: {i[0]}, Имя: {i[1]}, Фамилия: {i[2]}, Группа: {i[4]}")
        student_id = int(input("Введите ID студента, которого хотите отредактировать: "))
        student_info = database.get_student(student_id)
        print("Введите новые данные для студента:")
        first_name = input("Введите имя: ")
        last_name = input("Введите фамилию: ")
        middle_name = input("Введите отчество: ")
        group = input("Введите группу: ")
        grades_input = input("Введите оценки через запятую (5,5,5,5): ")
        grades = list(map(int, grades_input.split(',')))
        updated_student = Student(first_name, last_name, middle_name, group, grades)
        database.update_student(student_id, updated_student)
        updated_student_info = database.get_student(student_id)
    elif choice == 5:
        all_students = database.get_all_students()
        for i in all_students:
            print(f"ID: {i[0]}, Имя: {i[1]}, Фамилия: {i[2]}, Группа: {i[4]}")
        student_id = int(input("Введите ID студента, которого хотите удалить: "))
        database.delete_student(student_id)
        print("Студент удалён")
    elif choice == 6:
        group_name = input("Введите номер группы: ")
        print(f"Средний балл всей группы: {database.get_average_grade_group(group_name)}")
    elif choice == 7:
        break