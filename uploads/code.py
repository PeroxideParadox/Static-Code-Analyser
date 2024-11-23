# Sample code to test the analyzer
# Example of nested loops with conditional append
result = []
items=[]
unused_var = 42
used_var = 10
print(used_var)
for i in range(11):
    for j in range(10):
        if (i + j) % 2 == 0:
            result.append(i * j)
for i in range(len(items)):
    print(items[i])
# Example of inefficient list copy
original_list = [1, 2, 3, 4, 5]
copied_list = list(original_list)
print(copied_list)
# Example of multiple string concatenations
message = ""
message += "Hello, "
message += "world!"
message += " How are you?"
# Example of long if-elif chain
x = 5
if x == 1:
    print("One")
elif x == 2:
    print("Two")
elif x == 3:
    print("Three")
elif x == 4:
    print("Four")
elif x == 5:
    print("Five")
# Example of multiple list appends
