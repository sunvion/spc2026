students = {
    "김철수": 70,
    "이영희": 85,
    "박민수": 92,
    "최지우": 76,
    "정현우": 88,
    "한서연": 95,
    "오준호": 67,
    "윤가은": 81,
    "강도윤": 73,
    "송하린": 90
}

print(students)

def get_a_student(students):
    a_students = []
    for name, score in students.items(): # dict의 요소를 하나씩 가져옴 (items())
        if score >= 90:
            a_students.append(name)
    return a_students

print("A등급 학생: ", get_a_student(students))