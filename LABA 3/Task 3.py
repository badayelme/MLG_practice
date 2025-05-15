class Calculation:
    def __init__(self):
        self._calculationLine = ""

    def SetCalculationLine(self, new_calculationLine):
        self._calculationLine = new_calculationLine

    def SetLastSymbolCalculationLine(self, symbol):
        self._calculationLine += symbol

    def GetCalculationLine(self):
        return self._calculationLine

    def GetLastSymbol(self):
            return self._calculationLine[-1]

    def DeleteLastSymbol(self):
        calculation_list = list(self._calculationLine)
        calculation_list.pop()
        self._calculationLine = ''.join(calculation_list)

calculation = Calculation()

calculation.SetCalculationLine("10-5")
print(calculation.GetCalculationLine())

calculation.SetLastSymbolCalculationLine("=")
print(calculation.GetCalculationLine())

calculation.SetLastSymbolCalculationLine("5")
print(calculation.GetCalculationLine())

print(calculation.GetLastSymbol())

calculation.DeleteLastSymbol()
print(calculation.GetCalculationLine())