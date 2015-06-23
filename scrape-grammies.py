import csv, requests, re
from bs4 import BeautifulSoup

songArray = []
artistArray = []

def winningSong():
  f = csv.writer(open('grammies.csv', 'w'), delimiter = ';')
  url = 'http://en.wikipedia.org/wiki/Grammy_Award_for_Song_of_the_Year'
  html = requests.get(url).text
  soup = soup = BeautifulSoup(html)

  for i in soup.select('div#mw-content-text table.wikitable.sortable tr'):
    print 'Fetching some champs and putting them in a dusty CSV sheet'
    f.writerow([td.get_text(strip=True).encode('utf-8') for td in i.find_all(['th', 'td'])])

    for song in i.find_all('td')[2::4]:
      for songLink in song.find_all('a', href=True):
        songArray.append(songLink['href'])

    for artist in i.find_all('td')[3::4]:
      for artistLink in artist.find_all('a', href=True):
        artistArray.append(artistLink['href'])

  print 'Done writing Grammy winners to CSV'

def artist():
  fa = csv.writer(open('artist.csv', 'w'), delimiter = ';')
  for urli in artistArray:
    url = 'http://en.wikipedia.org' + urli
    html = requests.get(url).text
    soup = BeautifulSoup(html)

    # geboorteplaats
    for i in soup.select('table.infobox.vcard tr')[1:]:
      print 'Trying to solve where this artist is born...'
      born = i.find_all('th', text = 'Born').has_key('href')
      origin = i.find_all('th', text = 'Origin')

      print born
      
    # huidskleur


def song():
  fs = csv.writer(open('songs.csv', 'w'), delimiter = ';')
  for urli in songArray:
      url = 'http://en.wikipedia.org' + urli
      html = requests.get(url).text
      soup = BeautifulSoup(html)

      for i in soup.select('table.infobox.vevent tr')[1:]:
        print 'Writing song row'
        fs.writerow([td.get_text(strip=True).encode('utf-8') for td in i.find_all(['th', 'td'])])

  print 'Done writing songs to CSV'

winningSong()
artist()
print 'Done running script, check your files'