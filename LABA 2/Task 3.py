class Numbers:
    def __init__(self, num1, num2):
        self.num1 = num1
        self.num2 = num2

    def info(self):
        return (f"Первое число: {self.num1},\nВторое число: {self.num2},\n"
                f"Сумма чисел: {self.sum()},\nНаибольшее число: {self.max_value()}")

    def update_num1(self, new_num1):
        self.num1 = new_num1

    def update_num2(self, new_num2):
        self.num2 = new_num2

    def sum(self):
        return self.num1 + self.num2

    def max_value(self):
        return max(self.num1, self.num2)

num1 = int(input("Введите первое число: "))
num2 = int(input("Введите второе число: "))

numbers = Numbers(num1, num2)

while True:
    choice = int(input("1 - Вывести числа\n2 - Изменить числа\n3 - Завершить\n"))
    if choice == 1:
        print(numbers.info())
    elif choice == 2:
        choice_2 = int(input("1 - Первое число\n2 - Второе число\n3 - Выход: "))
        if choice_2 == 1:
            new_num1 = int(input("Введите новое первое число: "))
            numbers.update_num1(new_num1)
        elif choice_2 == 2:
            new_num2 = int(input("Введите новое второе число: "))
            numbers.update_num2(new_num2)
        elif choice_2 == 3:
            break
        else:
            print("Неверный выбор")
    elif choice == 3:
        break
    else:
        print("Неверный выбор.")