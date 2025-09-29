def add_two(num) :
    return num + 2

print(add_two(4))

result = add_two(8)
print(result)

def calculate(a, operation, b) :
    if operation is "+" :
        return a + b
    elif operation is "-" :
        return a - b 
    elif operation is "*" :
        return a * b
    else :
        return a / b
    
print(calculate(10, "+", 10))  # should return 20
print(calculate(10, "-", 10))  # should return 0
print(calculate(10, "*", 10))  # should return 100
print(calculate(10, "/", 10))  # should return 1.0

