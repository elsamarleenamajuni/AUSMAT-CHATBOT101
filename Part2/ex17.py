print("What is your name?")
name = input()

import random

adjectives = ['Stinky', 'Handsome', 'Scary']
animals = ['Snake', 'Crocodile', 'Cat']

print(name + ', your codename is: '+ random.choice(adjectives) + ' ' + random.choice(animals))
print('Your lucky number is: ' + str(random.randrange(0, 100)))