# Inefficient nested loops using range - excessive nesting
total_sum = 0
for a in range(10):
    for b in range(5):
        for c in range(3):
            total_sum += a + b

# Redundant sorting of the same list - unnecessary computation
data = [5, 3, 8, 1, 9]
data.sort()
data.sort(reverse=True)

# Repeated calculations - redundant computation
p = 4
result = (p * p) + (p * p) * 2

# Inefficient list appending - can be improved with list comprehension
generated_values = []
for i in range(5):
    generated_values.append(i ** 2)

# Long method - method with too many lines
def long_method():
    for i in range(50):
        print(i)
    # (Additional lines can be added here to exceed the threshold if needed)

# Large class - class with too many methods, potential to refactor
class LargeClass:
    def method1(self): pass
    def method2(self): pass
    def method3(self): pass
    def method4(self): pass
    def method5(self): pass
    def method6(self): pass
    def method7(self): pass
    def method8(self): pass
    def method9(self): pass
    def method10(self): pass
    def method11(self): pass

# Primitive Obsession - overly primitive data structures used directly
class DataContainer:
    def __init__(self):
        self.data_list = [1, 2, 3]
        self.data_dict = {"key": "value"}

# Data Clumps - repeated data elements that could be refactored into an object
class Address:
    def __init__(self, street, city, state, zip_code):
        self.street = street
        self.city = city
        self.state = state
        self.zip_code = zip_code

class Customer:
    def __init__(self, name, street, city, state, zip_code):
        self.name = name
        self.address = Address(street, city, state, zip_code)

# Long Parameter List - many parameters, suggests potential refactor to an object
def update_customer_details(name, address, phone_number, email, street, city, state, zip_code):
    pass

# Temporary Fields - fields used only in certain cases, creating unnecessary complexity
class Order:
    def __init__(self, order_id, customer_id):
        self.order_id = order_id
        self.customer_id = customer_id
        self.temp_discount = None

    def calculate_total(self):
        if self.temp_discount:
            pass

# Duplicated Code - code that repeats logic in multiple places
def calculate_total_amount(cart):
    total = 0
    for item in cart:
        total += item.price * item.quantity
    return total

def calculate_discount(cart):
    total_discount = 0
    for item in cart:
        total_discount += item.price * item.quantity * 0.1
    return total_discount

# Speculative Generality - unnecessary generalization without specific use
class GenericService:
    def process_data(self, data):
        pass

# Inappropriate Intimacy - class accessing data in another class too directly
class Customer:
    def __init__(self, name):
        self.name = name
        self.billing_address = Address('123 Main St', 'City', 'State', '12345')
    
    def print_address(self):
        print(self.billing_address.street, self.billing_address.city)

# Message Chains - overly long method chains
class Customer:
    def __init__(self, name):
        self.name = name
        self.billing_address = Address('123 Main St', 'City', 'State', '12345')

    def get_customer_street(self):
        return self.billing_address.get_street()

class Address:
    def __init__(self, street, city, state, zip_code):
        self.street = street
        self.city = city
        self.state = state
        self.zip_code = zip_code

    def get_street(self):
        return self.street

# Feature Envy - method accessing another class’s data excessively
class Address:
    def __init__(self, street, city, state, zip_code):
        self.street = street
        self.city = city
        self.state = state
        self.zip_code = zip_code

class Customer:
    def __init__(self, name, address):
        self.name = name
        self.address = address
    
    def print_full_address(self):
        print(f"{self.address.street}, {self.address.city}, {self.address.state}, {self.address.zip_code}")

# Lazy Class - class without sufficient functionality to justify existence
class Employee:
    def __init__(self, name):
        self.name = name

    def get_name(self):
        return self.name

# Middle Man - unnecessary delegation
class OrderProcessor:
    def __init__(self, order):
        self.order = order
    
    def process_order(self):
        self.order.submit_order()  # Unnecessary delegation

class Order:
    def submit_order(self):
        print("Order submitted")

# Inconsistent Naming - inconsistent variable names within a function
def calculate_data(data):
    result = 0
    for datum in data:
        result += datum
    return result

# Large Loop Bodies - loop with excessive lines of code
def process_data(data):
    for item in data:
        print(item)
        # Excessively long processing block here

# Unused Variables - variables declared but not used
unused_var = "This variable is never used"

# Magic Numbers - hardcoded numbers without context
tax_rate = 0.08  # Avoid magic numbers, use a constant or variable name

# Hardcoded Values - sensitive data hardcoded into the code
default_password = "1234"  # Avoid hardcoded passwords

# Improper Exception Handling - catching exceptions too broadly
try:
    result = 10 / 0
except:
    print("Error occurred")  # Catching all exceptions

# Dead Code - unreachable code
def compute_value(x):
    return x * 2
    print("This line is never reached")  # Dead code

# Large Static Initializers - large static configuration values
class Config:
    SETTINGS = {
        'url': 'http://example.com',
        'timeout': 5000,
        'max_retries': 3,
        'retry_interval': 300,
        # Excessive static configuration values
        # ...
    }