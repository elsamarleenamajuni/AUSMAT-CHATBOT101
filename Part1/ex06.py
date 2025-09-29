# List of names
names = ['Tom', 'Jerry', 'Butch', 'Tuffy', 'Pecos']

print(names)
print(*names)
for item in names:
    print(item)
print(", ".join(names))

first_item = names[0]
last_item = names[-1]
half = names[0:2]
back = names[-4:-1]
print(first_item)
print(last_item)
print(half)
print(back)