import csv, urllib2
from bs4 import BeautifulSoup

# CSV
f = csv.writer(open('grammies.csv', 'w'), delimiter = ';')
f.writerow(['Year', 'Category', 'Title', 'Winner'])

fa = csv.writer(open('wiki.csv', 'w'), delimiter = ';')
fa.writerow(['A', 'B', 'C'])

for numb in range(1, 161):
  url = 'http://www.grammy.com/nominees/search?page=' + str(numb)
  html = urllib2.urlopen(url).read()
  soup = BeautifulSoup(html)

  print 'Fetching item from grammy.com...'
  for item in soup.select('div.view-content table tr')[1:]:
    f.writerow([td.get_text(strip=True).encode('utf-8') for td in item.find_all('td')])
    
  for artist in item.select('a.freelink'):
    print 'Fetching data from Wikipedia...'
    artist = artist.text.replace(" ", "_").replace("&amp;", "&")
    wUrl = 'http://en.wikipedia.org/wiki/' + artist
    wHtml = urllib2.urlopen(wUrl).read()
    wSoup = BeautifulSoup(wHtml)

    for artist in wSoup.select('table.infobox tr')[1:]:
      fa.writerow([td.get_text(strip=True).encode('utf-8') for td in item.find_all('td')])