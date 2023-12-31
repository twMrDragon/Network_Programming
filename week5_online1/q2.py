import requests
from bs4 import BeautifulSoup

# 發票號碼網站前綴
baseUrl = 'https://www.etax.nat.gov.tw/etw-main/ETW183W2_1120'

# user input
n = int(input())
tickets = [input() for i in range(n)]
m = int(input())

# 爬網站
monthUrl = baseUrl+str(m-((m+1) % 2))+'/'
html = requests.get(monthUrl)
soup = BeautifulSoup(html.content, "html.parser")

# 找出獎項及中獎號碼
prices = {}
table = soup.find("table")
for i, v in enumerate(table.findAll('tr')[1:17]):
    if i >= 6:
        if i % 2 == 0:
            label = v.find('th').text
            prices[label] = {}
        else:
            prices[label]['des'] = v.find('td').text
    elif i % 2 == 0:
        label = v.find('th').text
        if label == '頭獎':
            prices[label] = {'number': [j.text.replace(' ', '').replace(
                '\n', '') for j in v.findAll('div', {'class': 'col-12 mb-3'})]}
        else:
            prices[label] = {'number': [v.find(
                'div', {'class': 'col-12 mb-3'}).text.replace(' ', '').replace('\n', '')]}
    else:
        prices[label]['des'] = v.find('td').text

# 數入個別中講金額
prices['特別獎']['get'] = 10_000_000
prices['特獎']['get'] = 2_000_000
prices['頭獎']['get'] = 200_000
prices['二獎']['get'] = 40_000
prices['三獎']['get'] = 10_000
prices['四獎']['get'] = 4_000
prices['五獎']['get'] = 1_000
prices['六獎']['get'] = 200

# 兌獎
getSum = 0
for ticket in tickets:
    hasPrice = False
    takeDig = 7
    headNumbers = prices['頭獎']['number']
    for i, v in prices.items():
        # 特別獎、特獎、頭獎
        if 'number' in v:
            for num in v['number']:
                if num == ticket:
                    print(ticket, i, v['des'])
                    getSum += v['get']
                    hasPrice = True
                    break
            if hasPrice:
                break
        # 剩下獎項(跟頭獎筆調尾n個數字的獎項)
        else:
            for headNum in headNumbers:
                if ticket[-takeDig:] == headNum[-takeDig:]:
                    getSum += v['get']
                    print(ticket, i, v['des'])
                    break
            takeDig -= 1
            if hasPrice:
                break
# 列印總獲獎金額
print(getSum)
