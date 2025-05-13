J = input("Введите драгоценности: ")
S = input("Введите камни: ")
sum = 0
for i in S:
    if i in J:
        sum += 1
print(f"Количество драгоценностей: {sum}")