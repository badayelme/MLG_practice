class Class:
    def __init__(self, name="NoName"):
        self._name = name
        print(f"Объект {self._name} создан")

    def __del__(self):
        print(f"Объект {self._name} удален")

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name):
        self._name = new_name

while True:
    choice = input("Создать объект? (Да/Нет): ")
    if choice == 'Да':
        name = input("Введите имя объекта: ")
        example = Class(name)
        break
    elif choice == 'Нет':
        print("OK")
        break
    else:
        print("Error")
while True:
    choice_2 = int(input("1 - Редактировать обьект\n2 - Удалить обьект\nДействие: "))
    if choice_2 == 1:
            new_name = input("Введите новое имя объекта: ")
            example.name = new_name
            print(f"Имя объекта изменено на {example.name}")
    elif choice_2 == 2:
        del example
        break
    else:
        print("Error")