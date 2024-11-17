# Sample code to test the analyzer

# Example of nested loops with conditional append
result = []
items=[]

unused_var = 42
used_var = 10
print(used_var)
result = [i * j for i in range(11) for j in range(10) if (i + j) % 2 == 0]

for i, i in enumerate(items):
    print(items[i])

# Example of inefficient list copy
original_list = [1, 2, 3, 4, 5]
copied_list = original_list.copy()
print(copied_list)

# Example of multiple string concatenations
message = ""
message = "".join(['', 'Hello, ', 'world!', ' How are you?'])

# Example of long if-elif chain
x = 5
switch_dict = {
    x == 1: print('One'),
    x == 2: print('Two'),
    x == 3: print('Three'),
    x == 4: print('Four'),
    x == 5: print('Five')
}
result = switch_dict.get(True, 'default_value')
sorted_list = sorted(unsorted_list)
another_sorted_list = sorted(sorted_list)