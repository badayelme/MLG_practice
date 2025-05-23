class Calculation:
    def __init__(self):
        self.calculationLine = ""

    def SetCalculationLine(self, value):
        self.calculationLine = value

    def SetlastSymbolCalculationLine(self, symbol):
        self.calculationLine += symbol

    def GetCalculationLine(self):
        return self.calculationLine

    def GetLastSymbol(self):
        return self.calculationLine[-1]

    def DeleteLastSymbol(self):
        self.calculationLine = self.calculationLine[:-1]

calc = Calculation()

while True:
    choice = input("1 - Ввести выражение, 2 - Ввести символ, 3 - Удалить последний символ, 4 - Вывести выражение, 5 - Выйти")
    if choice == "1":
        exp = input("Ввести выражение: ")
        calc.SetCalculationLine(exp)
    elif choice == "2":
        symbol = input("Ввести символ: ")
        calc.SetlastSymbolCalculationLine(symbol)
    elif choice == "3":
        calc.DeleteLastSymbol()
    elif choice == "4":
        print("Выражение:", calc.GetCalculationLine())
    elif choice == "5":
        break