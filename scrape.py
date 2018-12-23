from lxml import html
import requests
from bs4 import BeautifulSoup


# GET SONG URLS
def get_song_urls(artist_name):
	artist_url = 'http://www.metrolyrics.com/' + artist_name + '-lyrics.html'
	page_response = requests.get(artist_url)
	page_content = BeautifulSoup(page_response.content, "html.parser")

	song_links = []
	all_links = page_content.find_all('a', {"class": "title"})

	for a in all_links:
		href = a['href']

		if artist_name in href:
			song_links.append(href)

	return song_links


# GET SONG LYRICS
def get_song_lyrics(url):
	page_response = requests.get(url)
	page_content = BeautifulSoup(page_response.content, "html.parser")
	verses = page_content.find_all('p', {"class": "verse"})

	verse_str = ""
	for verse in verses:
		verse_str += verse.text
		verse_str = verse_str.replace(',', '')

	verse_list = verse_str.encode("utf-8").splitlines()
	return verse_list


# WRITE TO FILE
def write_to_file(verse_list):
	with open('lyrics.csv','a+') as lyrics_file:
		for item in verse_list:
			if '[' not in item and '(' not in item:
				item = item.strip().replace("'", '').replace("?", '')
				lyrics_file.write(item + ',')
				print(item)

	lyrics_file.close()


# START
artist_array = ['frank-ocean']

for artist in artist_array:
	song_urls = get_song_urls(artist)
	for url in song_urls:
		verse_list = get_song_lyrics(url)
		write_to_file(verse_list)
