file = open('./text/slang.txt', 'r', encoding='utf-8')
data = []
while True:
    line = file.readline()
    if not line:
        break
    data.append(line)
file.close()

for record in data:
    record = record.split(",")
print(record)

text = "박지윤"
text2 = "씨발"
if text in record:
    print("1있음")
if text2 in record:
    print("2있음")