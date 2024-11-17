# Sample code to test the analyzer

# Example of redundant computation in a loop
squares = []
for i in range(10):
    for j in range(5):
        squares.append(i * i)

# Example of unused imports and variables
import math  # unused import
unused_variable = "This variable is never used"

# Example of inefficient dictionary access
data = {"a": 1, "b": 2, "c": 3}
for key in data.keys():
    if key == "b":
        print(data[key])

# Example of repeated file reads
with open("example.txt", "r") as f:
    lines = f.readlines()

with open("example.txt", "r") as f:
    content = f.read()

# Example of suboptimal string formatting
name = "Alice"
age = 25
info = name + " is " + str(age) + " years old."
print(info)

# Example of inefficient list comprehension
numbers = [1, 2, 3, 4, 5]
squared_numbers = [x * x for x in numbers]
even_squares = [x for x in squared_numbers if x % 2 == 0]

# Example of deeply nested conditions
value = 15
if value > 10:
    if value < 20:
        if value % 5 == 0:
            print("Value is divisible by 5 and between 10 and 20")

# Example of excessive logging
for i in range(5):
    print(f"Processing item {i}...")

# Example of inefficient use of sets
items = [1, 2, 3, 4, 1, 2]
unique_items = []
for item in items:
    if item not in unique_items:
        unique_items.append(item)
print(unique_items)

# Example of unnecessary variable assignment
result = 0
value = 42
result = value
print(result)
