print('Hello, python')
print('Hello', 'python')
print("Hello, " + 'python')
print('Hello, ' + 'python' + "!!")
num = 5
name = '홍길동'
print("Hello, {}".format(name))
print("Hello, {}. My lucky number is {}".format(name, num))
print("Hello, {0}. My lucky number is {1}".format(name, num))
print("Hello, {1}. My lucky number is {0}".format(name, num))
print("Hello, %s" % name)
print("Hello, %s" % name, end="")
print("홍길동", end="")
print("홍길동", end="++")
print("홍길동", end="\n")
# 주석 처리 단축키는 ctrl + /
"""
여기는 멀티 라인으로 긴 내용을 담을 수 있음.
사실은 주석이 아닌 그냥 여러 줄의 문자열임.
"""
multiline = """
여기는 멀티 라인으로 긴 내용을 담을 수 있음.
사실은 주석이 아닌 그냥 여러 줄의 문자열임.
"""
print(multiline)