import csv

# 약간 옛날 방식, 리스트로 데이터 관리
data = [
    ['Name','Age','City'], # 해당 = 첫번째줄
    ['John','25','Seoul'],
    ['James','23','Busan'],
    ['Bob','24','Seoul']
]

filename = 'data.csv'

# 좀더 모던 방식, Dict로 데이터 관리
with open(filename, 'w', newline="") as file:
    # file.write(str(data))
    csv_writer = csv.writer(file)
    csv_writer.writerows(data)

data2 = [
    {'Name':'John','Age':'25','City':'Seoul'},
    {'Name':'James','Age':'23','City':'Busan'},
    {'Name':'Bob','Age':'24','City':'Seoul'}
]

with open(filename,'w',newline="") as file:
    #headers = ['Name','Age','City']
    headers = data2[0].keys()
    csv_writer = csv.DictWriter(file, fieldnames=headers)
    csv_writer.writeheader()   # 첫 줄(header) 작성
    csv_writer.writerows(data2) # 여러 줄 데이터 작성