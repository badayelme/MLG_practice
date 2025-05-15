class Worker:
    def __init__(self, name, surname, rate, days):
        self._name = name
        self._surname = surname
        self._rate = rate
        self._days = days

    def GetSalary(self):
        return self._rate * self._days

    def get_name(self):
        return self._name

    def get_surname(self):
        return self._surname

    def get_rate(self):
        return self._rate

    def get_days(self):
        return self._days

workers = []

while True:
    choice = int(input("1 - Добавить сотрудника\n2 - Показать зарплату\n3 - Вывести список сотрудников\n4 - Выход\nВыберите действие: "))
    if choice == 1:
        name = input("Имя: ")
        surname = input("Фамилия: ")
        rate = int(input("Ставка за день: "))
        days = int(input("Отработанные дни: "))
        workers.append(Worker(name, surname, rate, days))
    elif choice == 2:
        print("Список сотрудников:")
        for i in range(len(workers)):
            print(f"{i + 1}. {workers[i].get_name()} {workers[i].get_surname()}")
            number = int(input("Номер сотрудника: ")) - 1
            print(f"Зарплата: {workers[number].GetSalary()}")
    elif choice == 3:
        print("Список сотрудников:")
        for i in range(len(workers)):
            print(f"{i + 1}. {workers[i].get_name()} {workers[i].get_surname()} {workers[i].get_rate()} {workers[i].get_days()}")
    elif choice == 4:
        break
