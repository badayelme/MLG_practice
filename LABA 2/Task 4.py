class Counter:
    def __init__(self, value=0):
        self._value = value

    def addition(self):
        self._value += 1

    def decrease(self):
        self._value -= 1

    @property
    def value_info(self):
        return self._value

first_counter = int(input("Введите начало счетчика (0 = по умолчанию): "))
if first_counter == 0:
    counter = Counter()
else:
    counter = Counter(first_counter)

while True:
    choice = int(input("1 - Увеличить на 1\n2 - Уменьшить на 1\n3 - Статус\n4 - Завершить\nДействие: "))
    if choice == 1:
        counter.addition()
        print("Счетчик увеличен на 1")
    elif choice == 2:
        counter.decrease()
        print("Счетчик уменьшен на 1")
    elif choice == 3:
        print(f"Счетчик: {counter.value_info}")
    elif choice == 4:
        break