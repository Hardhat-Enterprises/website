from django.core.management.base import BaseCommand
from home.models import CodeTemplate

class Command(BaseCommand):
    help = 'Populate the database with sample Python code templates'

    def handle(self, *args, **options):
        templates = [
            {
                'title': 'Hello World',
                'description': 'Write a simple program that prints "Hello, World!" to the console.',
                'category': 'basics',
                'difficulty': 'beginner',
                'template_code': '# Write a program that prints "Hello, World!"\nprint("Hello, World!")',
                'expected_output': 'Hello, World!',
                'hints': 'Use the print() function to display text.'
            },
            {
                'title': 'Basic Calculator',
                'description': 'Create a simple calculator that can add, subtract, multiply, and divide two numbers.',
                'category': 'basics',
                'difficulty': 'beginner',
                'template_code': '# Create a basic calculator\n# Define two numbers\na = 10\nb = 5\n\n# Perform calculations\nprint(f"Addition: {a} + {b} = {a + b}")\nprint(f"Subtraction: {a} - {b} = {a - b}")\nprint(f"Multiplication: {a} * {b} = {a * b}")\nprint(f"Division: {a} / {b} = {a / b}")',
                'expected_output': 'Addition: 10 + 5 = 15\nSubtraction: 10 - 5 = 5\nMultiplication: 10 * 5 = 50\nDivision: 10 / 5 = 2.0',
                'hints': 'Use arithmetic operators (+, -, *, /) to perform calculations.'
            },
            {
                'title': 'List Operations',
                'description': 'Create a list and perform various operations like adding, removing, and accessing elements.',
                'category': 'data_structures',
                'difficulty': 'beginner',
                'template_code': '# Create a list and perform operations\nfruits = ["apple", "banana", "cherry"]\n\n# Add an element\nfruits.append("orange")\n\n# Remove an element\nfruits.remove("banana")\n\n# Access elements\nprint(f"First fruit: {fruits[0]}")\nprint(f"All fruits: {fruits}")\nprint(f"Number of fruits: {len(fruits)}")',
                'expected_output': 'First fruit: apple\nAll fruits: [\'apple\', \'cherry\', \'orange\']\nNumber of fruits: 3',
                'hints': 'Use append() to add elements, remove() to delete elements, and len() to get the length.'
            },
            {
                'title': 'Function Definition',
                'description': 'Write a function that takes two parameters and returns their sum.',
                'category': 'basics',
                'difficulty': 'intermediate',
                'template_code': '# Define a function that adds two numbers\ndef add_numbers(a, b):\n    return a + b\n\n# Test the function\nresult = add_numbers(5, 3)\nprint(f"The sum is: {result}")',
                'expected_output': 'The sum is: 8',
                'hints': 'Use the def keyword to define a function and return to send back a value.'
            },
            {
                'title': 'Dictionary Operations',
                'description': 'Create a dictionary to store student information and perform various operations.',
                'category': 'data_structures',
                'difficulty': 'intermediate',
                'template_code': '# Create a student dictionary\nstudent = {\n    "name": "John Doe",\n    "age": 20,\n    "grade": "A"\n}\n\n# Add new information\nstudent["subject"] = "Computer Science"\n\n# Update existing information\nstudent["age"] = 21\n\n# Display information\nfor key, value in student.items():\n    print(f"{key}: {value}")',
                'expected_output': 'name: John Doe\nage: 21\ngrade: A\nsubject: Computer Science',
                'hints': 'Use curly braces {} to create dictionaries and for loops to iterate through them.'
            },
            {
                'title': 'Class Definition',
                'description': 'Create a simple class with methods to represent a bank account.',
                'category': 'oop',
                'difficulty': 'intermediate',
                'template_code': '# Create a BankAccount class\nclass BankAccount:\n    def __init__(self, account_holder, initial_balance=0):\n        self.account_holder = account_holder\n        self.balance = initial_balance\n    \n    def deposit(self, amount):\n        self.balance += amount\n        return self.balance\n    \n    def withdraw(self, amount):\n        if amount <= self.balance:\n            self.balance -= amount\n            return self.balance\n        else:\n            return "Insufficient funds"\n\n# Test the class\naccount = BankAccount("Alice", 1000)\nprint(f"Initial balance: {account.balance}")\naccount.deposit(500)\nprint(f"After deposit: {account.balance}")\nresult = account.withdraw(200)\nprint(f"After withdrawal: {result}")',
                'expected_output': 'Initial balance: 1000\nAfter deposit: 1500\nAfter withdrawal: 1300',
                'hints': 'Use class keyword to define a class, __init__ for constructor, and self to refer to the instance.'
            },
            {
                'title': 'File Reading',
                'description': 'Write a program that reads content from a file and displays it.',
                'category': 'file_handling',
                'difficulty': 'intermediate',
                'template_code': '# Read content from a file\n# Note: This is a simulation since we can\'t create actual files in the compiler\n# In real scenarios, you would use: with open("filename.txt", "r") as file:\n\n# Simulate file content\nfile_content = "Hello from file!\\nThis is line 2.\\nThis is line 3."\n\n# Process the content\nlines = file_content.split("\\n")\nprint(f"Number of lines: {len(lines)}")\nfor i, line in enumerate(lines, 1):\n    print(f"Line {i}: {line}")',
                'expected_output': 'Number of lines: 3\nLine 1: Hello from file!\nLine 2: This is line 2.\nLine 3: This is line 3.',
                'hints': 'Use split() to separate lines and enumerate() to get both index and value.'
            },
            {
                'title': 'Exception Handling',
                'description': 'Write a program that handles division by zero and other exceptions gracefully.',
                'category': 'basics',
                'difficulty': 'intermediate',
                'template_code': '# Handle exceptions gracefully\ndef safe_divide(a, b):\n    try:\n        result = a / b\n        return result\n    except ZeroDivisionError:\n        return "Cannot divide by zero!"\n    except TypeError:\n        return "Invalid input types!"\n    except Exception as e:\n        return f"An error occurred: {e}"\n\n# Test the function\nprint(safe_divide(10, 2))\nprint(safe_divide(10, 0))\nprint(safe_divide("10", 2))',
                'expected_output': '5.0\nCannot divide by zero!\nInvalid input types!',
                'hints': 'Use try-except blocks to catch and handle different types of exceptions.'
            },
            {
                'title': 'List Comprehension',
                'description': 'Use list comprehension to create a list of squares of numbers from 1 to 10.',
                'category': 'data_structures',
                'difficulty': 'advanced',
                'template_code': '# Create a list of squares using list comprehension\nsquares = [x**2 for x in range(1, 11)]\nprint(f"Squares from 1 to 10: {squares}")\n\n# Filter even squares\neven_squares = [x**2 for x in range(1, 11) if x % 2 == 0]\nprint(f"Even squares: {even_squares}")\n\n# Create a dictionary using dictionary comprehension\nsquare_dict = {x: x**2 for x in range(1, 6)}\nprint(f"Square dictionary: {square_dict}")',
                'expected_output': 'Squares from 1 to 10: [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]\nEven squares: [4, 16, 36, 64, 100]\nSquare dictionary: {1: 1, 2: 4, 3: 9, 4: 16, 5: 25}',
                'hints': 'List comprehension syntax: [expression for item in iterable if condition]'
            },
            {
                'title': 'Recursive Function',
                'description': 'Write a recursive function to calculate the factorial of a number.',
                'category': 'algorithms',
                'difficulty': 'advanced',
                'template_code': '# Recursive factorial function\ndef factorial(n):\n    if n == 0 or n == 1:\n        return 1\n    else:\n        return n * factorial(n - 1)\n\n# Test the function\nfor i in range(1, 6):\n    result = factorial(i)\n    print(f"Factorial of {i} is {result}")',
                'expected_output': 'Factorial of 1 is 1\nFactorial of 2 is 2\nFactorial of 3 is 6\nFactorial of 4 is 24\nFactorial of 5 is 120',
                'hints': 'A recursive function calls itself with a smaller input until it reaches a base case.'
            }
        ]

        created_count = 0
        for template_data in templates:
            template, created = CodeTemplate.objects.get_or_create(
                title=template_data['title'],
                defaults=template_data
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created template: {template.title}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Template already exists: {template.title}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} new templates!')
        )

