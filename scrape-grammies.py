import csv, urllib2
from bs4 import BeautifulSoup

f = csv.writer(open('grammies.csv', 'w'))
f.writerow(['Year', 'Category', 'Title', 'Winner'])

for numb in range(1, 161):
  url = 'http://www.grammy.com/nominees/search?page=' + str(numb)
  html = urllib2.urlopen(url).read()
  soup = BeautifulSoup(html)

  for item in soup.select('div.view-content table tr')[1:]:
    f.writerow([td.get_text(strip=True).encode('utf-8') for td in item.find_all('td')])