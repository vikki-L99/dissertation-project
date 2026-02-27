TEST_CASES = [
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
	{
		"id": "TC005",
		"description": "String concatenation with integer",
		"buggy_code": """
age = 20
print("I am " + age + " years old")
"""
	}
]