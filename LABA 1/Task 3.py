nums = [1,2,3,4,5,1]
print(nums)
if len(nums) == len(set(nums)):
    print("False")
else:
    print("True")