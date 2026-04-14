# ============================================================
# test_cases.py - Buggy Python Code Test Cases
#
# Contains 20 buggy Python code scenarios used as inputs
# for the benchmarking framework. Each test case represents
# a common mistake made by novice Python programmers.
#
# Each test case has three fields:
#   - id:          Unique identifier (TC001 to TC020)
#   - description: Brief description of the bug type
#   - buggy_code:  The Python code containing the bug
#
# Test cases are organised across 10 error categories:
#   1. Division / ZeroDivision errors    (TC001, TC011)
#   2. Index / Range errors              (TC002, TC012)
#   3. Mutable default arguments         (TC003)
#   4. Logic / Indentation errors        (TC004, TC015)
#   5. Type errors                       (TC005, TC017)
#   6. Variable scope errors             (TC006, TC013)
#   7. Infinite loops                    (TC007, TC014)
#   8. Missing return values             (TC008)
#   9. List mutation during iteration    (TC009)
#  10. Boolean logic errors              (TC010)
#  11. List method misuse                (TC016)
#  12. String/integer comparison         (TC018)
#  13. Dictionary key errors             (TC019)
#  14. Variable shadowing                (TC020)
# ============================================================

TEST_CASES = [

	# --- Category 1: Division / ZeroDivision Errors ---

	{
		"id": "TC001",
		"description": "Division by zero with empty list",
		"buggy_code": """
def calculate_average(numbers):
	total = 0
	for n in numbers:
		total = total + n
	return total / len(numbers)

print(calculate_average([]))
"""
	},

	# --- Category 2: Index / Range Errors ---

	{
		"id": "TC002",
		"description": "Off-by-one error in loop",
		"buggy_code": """
def print_items(items):
	for i in range(len(items) + 1):
		print(items[i])

print_items([1, 2, 3])
"""
	},

	# --- Category 3: Mutable Default Arguments ---

	{
		"id": "TC003",
		"description": "Mutable default argument",
		"buggy_code": """
def add_item(item, my_list=[]):
	my_list.append(item)
	return my_list

print(add_item(1))
print(add_item(2))
"""
	},

	# --- Category 4: Logic / Indentation Errors ---

	{
		"id": "TC004",
		"description": "Wrong indentation in conditional",
		"buggy_code": """
def check_positive(number):
	if number > 0:
		print("Positive")
	return True

print(check_positive(-5))
"""
	},

	# --- Category 5: Type Errors ---

	{
		"id": "TC005",
		"description": "String concatenation with integer",
		"buggy_code": """
age = 20
print("I am " + age + " years old")
"""
	},

	# --- Category 6: Variable Scope Errors ---

	{
		"id": "TC006",
		"description": "Variable scope error",
		"buggy_code": """
def set_value():
	x = 10

set_value()
print(x)
"""
	},

	# --- Category 7: Infinite Loops ---

	{
		"id": "TC007",
		"description": "Infinite loop missing update",
		"buggy_code": """
def count_down(n):
	while n > 0:
		print(n)

count_down(5)
"""
	},

	# --- Category 8: Missing Return Values ---

	{
		"id": "TC008",
		"description": "Function returns None instead of value",
		"buggy_code": """
def multiply(a, b):
	result = a * b

print(multiply(3, 4))
"""
	},

	# --- Category 9: List Mutation During Iteration ---

	{
		"id": "TC009",
		"description": "List modified during iteration",
		"buggy_code": """
numbers = [1, 2, 3, 4, 5]
for n in numbers:
	if n % 2 == 0:
		numbers.remove(n)

print(numbers)
"""
	},

	# --- Category 10: Boolean Logic Errors ---

	{
		"id": "TC010",
		"description": "Wrong boolean logic with or",
		"buggy_code": """
def is_valid_age(age):
	if age < 0 or age > 150:
		return False
	return True

print(is_valid_age(-1))
print(is_valid_age(200))
"""
	},

	# --- Category 1 (continued): Division / ZeroDivision Errors ---

	{
		"id": "TC011",
		"description": "Second division by zero variant",
		"buggy_code": """
def percentage(part, total):
	return (part / total) * 100

print(percentage(50, 0))
"""
	},

	# --- Category 2 (continued): Index / Range Errors ---

	{
		"id": "TC012",
		"description": "String index out of range",
		"buggy_code": """
def get_last_char(s):
	return s[len(s)]

print(get_last_char("hello"))
"""
	},

	# --- Category 6 (continued): Variable Scope Errors ---

	{
		"id": "TC013",
		"description": "Incorrect use of global variable",
		"buggy_code": """
counter = 0

def increment():
	counter += 1

increment()
print(counter)
"""
	},

	# --- Category 7 (continued): Infinite Loops ---

	{
		"id": "TC014",
		"description": "Infinite loop with wrong condition",
		"buggy_code": """
def find_first_even(numbers):
	i = 0
	while numbers[i] % 2 != 0:
		print(numbers[i])
	return numbers[i]

print(find_first_even([1, 3, 5, 4]))
"""
	},

	# --- Category 4 (continued): Logic / Indentation Errors ---

	{
		"id": "TC015",
		"description": "Return inside loop exits too early",
		"buggy_code": """
def sum_list(numbers):
	for n in numbers:
		total = 0
		total += n
	return total

print(sum_list([1, 2, 3, 4]))
"""
	},

	# --- Category 11: List Method Misuse ---

	{
		"id": "TC016",
		"description": "List append result assigned to variable",
		"buggy_code": """
numbers = [1, 2, 3]
numbers = numbers.append(4)
print(numbers)
"""
	},

	# --- Category 5 (continued): Type Errors ---

	{
		"id": "TC017",
		"description": "Comparing string to integer",
		"buggy_code": """
user_input = "5"
if user_input == 5:
	print("Five!")
else:
	print("Not five")
"""
	},

	# --- Category 12: String/Integer Comparison ---

	{
		"id": "TC018",
		"description": "Wrong use of equality vs assignment",
		"buggy_code": """
def check_zero(n):
	if n = 0:
		return True
	return False

print(check_zero(0))
"""
	},

	# --- Category 13: Dictionary Key Errors ---

	{
		"id": "TC019",
		"description": "Dictionary key error",
		"buggy_code": """
student = {"name": "Alice", "grade": 90}
print(student["age"])
"""
	},

	# --- Category 14: Variable Shadowing ---

	{
		"id": "TC020",
		"description": "Nested loop variable shadowing",
		"buggy_code": """
def print_pairs(n):
	for i in range(n):
		for i in range(n):
			print(i, i)

print_pairs(3)
"""
	}

]