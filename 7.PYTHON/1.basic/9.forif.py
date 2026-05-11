numbers = [1,2,3,4,5]

for num in numbers:
    if num % 2 == 0:
        print(f'숫자 {num}은 짝수입니다.')
    else:
        print(f'숫자 {num}은 홀수입니다.')

even_numbers = []
odd_numbers = []

for num in numbers:
    if num % 2 == 0:
        even_numbers.append(num)
    else:
        odd_numbers.append(num)

print(f'짝수: {even_numbers}')
print(f'홀수: {odd_numbers}')

import time

n = 100
count = 0

start_time = time.time()

for a in range(n):
    for b in range(n):
        for c in range(n):
            for d in range(n):
                count += 1

end_time = time.time()

exec_time = end_time - start_time

print('합산:', count)
print('실행 시간:', exec_time)