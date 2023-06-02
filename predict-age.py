print('This program guess your age & your desired number \njust choose a number and follow steps')
input('Select a number and press enter...')
input('Now, mines 1...')
input('multiple in 100...')
input('Add your age to the number...')
input('Add 9 to your number...')
input('mines 1020 from your answer...')

res = int(input('Answer: '))
res += 1111

number = str(res)[:2]
age = str(res)[2:4]

print(f'\nYour age: {age} \nYour number: {number}')
