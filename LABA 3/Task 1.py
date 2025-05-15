class Worker:
    def __init__(self, name, surname, rate, days):
        self.name = name
        self.surname = surname
        self.rate = rate
        self.days = days

    def GetSalary(self):
        return self.rate * self.days

workers = []

while True:
    choice = int(input("1 - Добавить сотрудника\n2 - Показать зарплату\n3 - Завершить\nДействие: "))
    if choice == 1:
        name = input("Имя: ")
        surname = input("Фамилия: ")
        rate = int(input("Ставка за день: "))
        days = int(input("Отработанные дни: "))
        workers.append(Worker(name, surname, rate, days))
    elif choice == 2:
        print("Список сотрудников:")
        for i in range(len(workers)):
            print(f"{i + 1}. {workers[i].name} {workers[i].surname}")
            number = int(input("Номер сотрудника: ")) - 1
            print(f"Зарплата: {workers[number].GetSalary()}")
    elif choice == 3:
        break
