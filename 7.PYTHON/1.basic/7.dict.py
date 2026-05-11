# 딕셔너리
# 키:밸류로 쌍을 이루고 있는 자료 구조
my_dict = {"name":"Alice", "age":25, "location":"서울"}
print(my_dict)

# JSON과 비슷하게 생겨서 웹 서비스 만들 때 많이 사용함, 그렇다고 JSON은 아님.
print(my_dict['name']) # Alice가 찍힘
print(my_dict['age']) # 25가 찍힘

my_dict["car"]="BMW"
print(my_dict)

del my_dict["location"] # del을 사용한 거라 문법이 이상함
print(my_dict)

my_dict.pop('age') # pop도 가능함
print(my_dict)

my_dict.clear() # 모든 멤버 다 지우기
print(my_dict)

"""
리스트는 [] 대괄호 = 일반리스트
튜플은 () 소괄호 = 읽기전용 리스트
딕셔너리 {} 중괄호 = 키밸류 리스트
"""

# dict의 기본은 keys:value 쌍의 저장
my_squares = {x: x**2 for x in range(10)}
print(my_squares)

print(my_squares.keys())
print(my_squares.values())