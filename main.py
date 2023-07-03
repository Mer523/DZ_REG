from pprint import pprint
import re
import csv

with open("phonebook_raw.csv", encoding='utf-8') as file:
    rows = csv.reader(file, delimiter=",")
    contacts_list = list(rows)
pprint(contacts_list)

phone_pattern = re.compile(
    r'(\+7|8)\s*\(*(\d{3})\)*\s*\-*(\d{3})\s*\-*(\d{2})\s*\-*(\d{2})')
extension_pattern = re.compile(r'\s*\(*(доб.)\s*(\d+)\)*\s*')
text_pattern = re.compile(
    r'(\w+[А-яЁё])\s*\,*(\w+[А-яЁё])\s*\,*(\w+[А-яЁё])*\,*(\w+[А-яЁё])*\,*(\w+[А-яЁё]\w+[А-яЁё –]*'
    r'\–*\s*)*\,*(\+*\d\s*\(*\d+\)*\-*\s*\d+\-*\d+\-*\d+\s*\(*\w*\.*\s*\d*\)*)*\,*([a-zA-Z0-9_.+-]'
    r'+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)*')

new_list = []
for c in range(len(contacts_list)):
    if c == 0:
        new_list.append(contacts_list[c])
    else:
        line = ','.join(contacts_list[c])
        result = re.search(text_pattern, line)
        new_list.append(list(result.groups()))
        if new_list[c][5] is not None:
            new_list[c][5] = phone_pattern.sub(r'+7(\2)\3-\4-\5', new_list[c][5])
            new_list[c][5] = extension_pattern.sub(r' \1\2', new_list[c][5])

final_list = []
for i in range(len(new_list)):
    for s in range(len(new_list)):
        if new_list[i][0] == new_list[s][0]:
            new_list[i] = [x or y for x, y in zip(new_list[i], new_list[s])]
        if new_list[i] not in final_list:
            final_list.append(new_list[i])

with open("phonebook.csv", "w") as file:
    datawriter = csv.writer(file, delimiter=',')
    datawriter.writerows(final_list)