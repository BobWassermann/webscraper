import csv, requests, re
from bs4 import BeautifulSoup

# urls
songArray = []
artistArray = []

# content
artistNameArray = []
artistBornArray = []

songNameArray = []
songGenreArray = []
songLabelArray = []
songLengthArray = []

def winningSong():
  f = csv.writer(open('grammies.csv', 'w'), delimiter = ';')
  url = 'http://en.wikipedia.org/wiki/Grammy_Award_for_Song_of_the_Year'
  html = requests.get(url).text
  soup = soup = BeautifulSoup(html)

  for i in soup.select('div#mw-content-text table.wikitable.sortable tr'):
    # print 'Fetching some champs and putting them in a dusty CSV sheet'
    f.writerow([td.get_text(strip=True).encode('utf-8') for td in i.find_all(['th', 'td'])])

    for song in i.find_all('td')[2::4]:
      for songLink in song.find_all('a', href=True):
        songArray.append(songLink['href'])

    for artist in i.find_all('td')[3::4]:
      if artist.find('a'):
        artistArray.append(artist.find('a').get('href'))
      else:
        artistArray.append('/wiki/Various_Artists')

  # print 'Done writing Grammy winners to CSV'

def artist():
  for urli in artistArray:
    url = 'http://en.wikipedia.org' + urli
    html = requests.get(url).text
    soup = BeautifulSoup(html)

    # naam
    for i in soup.select('h1.firstHeading'):
      artistNameArray.append(i.text)
    
    # geboren
    if url != 'http://en.wikipedia.org/wiki/Various_Artists':
      if soup.find('th', text = 'Born'):
        if soup.find('th', text = 'Born').findNext('td').find('a'):
          artistBornArray.append(soup.find('th', text = 'Born').findNext('td').find('a').text)
        else:
          artistBornArray.append(soup.find('th', text = 'Origin').findNext('td').find('a').text)
      elif soup.find('th', text = 'Origin'):
        if soup.find('th', text = 'Origin').findNext('td').find('a'):
          artistBornArray.append(soup.find('th', text = 'Origin').findNext('td').find('a').text)
        else:
          artistBornArray.append(soup.find('th', text = 'Origin').findNext('td').text)
    else:
      artistBornArray.append('-') 


def song():
  for urli in songArray:
      url = 'http://en.wikipedia.org' + urli
      html = requests.get(url).text
      soup = BeautifulSoup(html)

      # Song name
      if urli != '/wiki/Rodney_Jerkins':
        if soup.select('h1.firstHeading'):
          for i in soup.select('h1.firstHeading'):
            songNameArray.append(i.text)
            print i.text

      # Songe genre
        if (urli == '/wiki/Exodus_(1960_film)') or (urli == '/wiki/The_Shadow_of_Your_Smile'):
          songGenreArray.append('Jazz')
        elif soup.select('div#mw-content-text table.infobox'):
          if soup.find('th', text = 'Genre'):
            songGenreArray.append(soup.find('th', text = 'Genre').findNext('td').text)
          else:
            songGenreArray.append('-')
        else:
          songGenreArray.append('-')

      # Length
        if soup.select('div#mw-content-text table.infobox'):
          for i in soup.select('div#mw-content-text table.infobox'):
            if i.find('th', text = 'Length'):
              songLengthArray.append(i.find('th', text = 'Length').findNext('td').text)
              print i.find('th', text = 'Length').findNext('td').text
            else:
              songLengthArray.append('-')
              print '-'
            break
        else:
          songLengthArray.append('-')

        # Label
        if soup.select('div#mw-content-text table.infobox'):
          for i in soup.select('div#mw-content-text table.infobox'):
            if i.find('th', text = 'Label'):
              songLabelArray.append(i.find('th', text = 'Label').findNext('td').text)
            else:
              songLabelArray.append('-')
            break
        else:
          songLabelArray.append('-')

  print 'Done writing songs to CSV'

print 'Started scrape, a truh mastah piece. Breh breh.'
winningSong()
artist()
song()

fs = csv.writer(open('masterscrape.csv', 'w'), delimiter = ';')
fs.writerow([td.encode('utf-8') for td in artistNameArray])
fs.writerow([td.encode('utf-8') for td in artistBornArray])
fs.writerow([td.encode('utf-8') for td in songNameArray])
fs.writerow([td.encode('utf-8') for td in songGenreArray])
fs.writerow([td.encode('utf-8') for td in songLengthArray])
fs.writerow([td.encode('utf-8') for td in songLabelArray])
print 'Done running script, check your files'