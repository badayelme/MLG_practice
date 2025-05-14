class Class:
    def __init__(self, name="NoName"):
        self.name = name
        print(f"Объект {self.name} создан")

    def __del__(self):
        print(f"Объект {self.name} удален")

while True:
    object = input("Создать объект? (Да/Нет): ").lower()
    if object == 'да':
        example = Class()
        break
    elif object == 'нет':
        print("OK")
        break
    else:
        print("Error")