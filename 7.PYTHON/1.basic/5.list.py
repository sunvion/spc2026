my_list = [1,2,3,4,5]

print(my_list)
print(len(my_list))

print(my_list[0]) # 모든 언어의 첫번째 멤버는 0번임
print(my_list[4]) # 4번이 다섯번째 멤버
# print(my_list[5]) # 5번이 여섯번째 멤버

print(my_list[-1]) # 리스트의 역순 (뒤로, 마지막)
print(my_list[-2]) # 뒤에서 두번째

print(my_list[1:3]) # 슬라이싱 [1] 포함하고 [3] 포함하지 않음
print(my_list[3:5]) # 슬라이싱 [3] 포함하고 [5] 포함하지 않음
print(my_list[:2]) # 시작부터 [2]를 포함하지 않음
print(my_list[2:]) # [2]부터 끝까지

# 원본 리스트에 멤버 추가하기
my_list.append(6)
print(my_list)

# 특정 위치에 멤버 추가하기
my_list.insert(2, 99) # [2]에 추가
print(my_list)

# 해당 값의 요소 삭제하기
my_list.remove(99)
print(my_list)

# 특정 인덱스의 요소 삭제하기
my_list.pop(3) # [3] 인덱스 삭제
print(my_list)

my_list.pop() # 인덱스를 안 넣으면 기본적으로 맨 뒤를 삭제
print(my_list)

my_list.clear() # 리스트 통째로 비우기
print(my_list)

my_list = [5,2,1,3,4,7,6,8,9]
print(my_list)

my_list.sort() # 정렬을 하는데, 원본값을 변경하는 함수
print(my_list)

my_list = [5,2,1,3,4,7,6,8,9]
new_list = sorted(my_list) # 원본을 유지하고 복제본을 만듬
print(my_list)
print(new_list)

copyed_list = my_list.copy() # 원본 리스트의 복제본을 만듬
print(copyed_list)
copyed_list.sort(reverse=True)
print(copyed_list)
print(my_list)

# 리스트 컴프리헨션 (어려운데, 쓰면 매우매우 편함)
print("-" * 30)
numbers = [x for x in range(1,10)]
print(numbers)
numbers = [x for x in range(5)] # 시작 값은 0
print(numbers)
numbers = [x**2 for x in range(5)] # 이전값의 제곱수들이 포함된 리스트
print(numbers)
numbers = [x for x in range(1,10)] # 1부터 9까지의 값
print(numbers)
numbers = [x for x in range(1,10) if x % 2 == 0] # x를 2로 나눈 나머지가 0이면 짝수
print(numbers)
numbers = [x for x in range(1,10) if x % 2 == 1] # x를 2로 나눈 나머지가 1이면 홀수
print(numbers)
numbers = [x      for x in range(1,10)      if x % 2 == 1] # 띄워도 읽음
print(numbers)

list1 = [1,2,3]
list2 = [4,5,6]

list12 = list1 + list2 # 리스트의 합산
print(list12)
print(list1 * 3) # 리스트 자체의 곱(즉 반복)