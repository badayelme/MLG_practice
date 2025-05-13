candidates = [10,1,2,7,6,1,5]
target = 8
result = []

for i in range(len(candidates)):
    if candidates[i] == target:
        result.append([candidates[i]])
    for j in range(i, len(candidates)):
        if candidates[i] + candidates[j] == target:
            result.append([candidates[i], candidates[j]])
        for o in range(j, len(candidates)):
            if candidates[i] + candidates[j] + candidates[o] == target:
                result.append([candidates[i], candidates[j], candidates[o]])
            for l in range(o, len(candidates)):
                if candidates[i] + candidates[j] + candidates[o] + candidates[l] == target:
                    result.append([candidates[i], candidates[j], candidates[o], candidates[l]])
result = [list(combo) for combo in {tuple(combo) for combo in result}]
print(result)