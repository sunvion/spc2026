users = [
    {"name": "김철수", "age": 25, "location": "서울", "car": "소나타"},
    {"name": "이영희", "age": 31, "location": "부산", "car": "아반떼"},
    {"name": "박민수", "age": 28, "location": "인천", "car": "K5"},
    {"name": "최지우", "age": 22, "location": "대전", "car": "모닝"},
    {"name": "정현우", "age": 40, "location": "대구", "car": "그랜저"},
    {"name": "한서연", "age": 27, "location": "광주", "car": "셀토스"},
    {"name": "김준호", "age": 40, "location": "울산", "car": "싼타페"},
    {"name": "윤가은", "age": 24, "location": "수원", "car": "레이"},
    {"name": "강도윤", "age": 33, "location": "제주", "car": "EV6"},
    {"name": "송하린", "age": 29, "location": "청주", "car": "투싼"}
]

def find_user_and_print(name):
    for user in users:
        # if user['name'] == name: # 정확한 매칭 찾기
        if user['name'].startswith(name): # 앞글자 즉 성으로 찾기
            print(user)

find_user_and_print('김')
find_user_and_print('한')

print('-' * 30)

def find_user_and_return(name):
    found = [] # 찾은 사용자를 담을 바구니(리스트 변수)
    for user in users:
        if user['name'].startswith(name):
            found.append(user)
    return found

# found_users = find_user_and_return('김')
# found_users = find_user_and_return('한')
found_users = find_user_and_return('구')
print('찾은 사용자: ', found_users)

def find_users2(name=None, age=None):
    """이름 또는 나이를 입력받아 매칭되는 사람을 반환한다."""
    found = []

    for user in users:
        if name is not None and age is not None:
            if user['name'] == name and user['age'] == age:
                found.append(user)
        elif name is not None:
            if user['name'] == name:
                found.append(user)
        elif age is not None:
            if user['age'] == age:
                found.append(user)
    return found

print(find_users2('김준호'))
print(find_users2('김준호', 40))
print(find_users2('김준호', 30))
print(find_users2(age=40)) # 나이로만 찾으려면 어떻게?

print('-'*30)
def find_user2_better(name=None, age=None, location=None):
    """이름 또는 나이를 입력바아 매칭되는 사람을 반환한다."""
    found = []
    for user in users:
        #        true    or  비교문
        if (name is None or user['name']==name) \
            and (age is None or user['age']==age) \
            and (location is None or user['location']==location):
            found.append(user)
    return found

print(find_user2_better('김준호'))
print(find_user2_better('김준호', 40, '울산'))
print(find_user2_better('김준호', 30))
print(find_user2_better(age=40)) # 나이로만 찾으려면 어떻게?

print('-' * 30)

search_condition1 = {
    'name': '김준호'
}

search_condition1 = {
    'name': '김준호',
    'age': 40
}

search_condition3 = {
    'age': 40
}

# def find_users2_best(condition):
#     found = []
#     for user in users:
#         if user.get('name') == condition.get('name', "") \
#         and user.get('age') == condition.get('age', 0) \
#         and user.get('location') == condition.get('location', ""):
#             found.append(user)

#     return found

# print(find_users2_best(search_condition1))