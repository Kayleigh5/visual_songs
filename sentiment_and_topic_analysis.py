#!/usr/bin/python
import cgi, cgitb 
import lyrics_scraper
import nltk
import yaml
import sentiment_analysis
import re
import os
import urllib2
import urllib
from bs4 import BeautifulSoup
from nltk.probability import FreqDist
from nltk.corpus import stopwords
import sys, time

sys.stdout.write('Content-Type: text/html;charset=utf-8\r\n\r\n')
isloading = "<p class=\"place\">placeholder</p>"
downloading_images = "<p class=\"place\">downloading images</p>"

print "<head>"
print "<link  href=\"css.css\" rel=\"stylesheet\" type=\"text/css\">"
print "<link href=\"bootstrap.min.css\" rel=\"stylesheet\" type=\"text/css\">"
print "<script src=\"jquery-1.9.1.min.js\"></script>"
print "<script>"
print "$(document).ready(function(){"
print "$(\"h1\").html('THE RESULTS');"
print "});"
print "</script>"
print "<title>Visual Songs</title>"
print "</head>"
print "<html>"
print "<body>"
print "<div id=\"home\" class=\"fullscreen\">"
print "<div class=\"text-vcenter text-home\">"
print "<div class=\"col-lg-8 col-lg-offset-2 col-md-8 col-md-offset-2 col-sm-8 col-sm-offset-2\">"
print "<h1>Wait a minute while the application is loading...</h1>"

# get input from user form
form = cgi.FieldStorage() 
lyrics_scraper.artist_name_search = form.getvalue('artist_name')
artist_name = lyrics_scraper.artist_name_search
dicttagger = sentiment_analysis.DictionaryTagger([ 'dicts/negative_dictionary.yml', 'dicts/positive_dictionary.yml', 'dicts/inc.yml', 'dicts/dec.yml', 'dicts/inv.yml'])

# crawl the lyrics
lyrics_scraper.crawl()
songtext = lyrics_scraper.pipeline.lyrics_array
if len(songtext) < 40:
	songtext = songtext[0::]
else:
	songtext = songtext[0:40]

songtext_file = open("scrape_result.txt", 'w')
songtext_file.write(str(songtext))


# KAYLEIGH
full_songtext = open('scrape_result.txt')						#songtext openen
full_songs = full_songtext.read()									#songtext inlezen
full_songs = full_songs.lower()									#hoofdletters verwijderen
full_songs = full_songs.replace('{', ' ')		                       #tekst schoonmaken
full_songs = full_songs.replace('[', ' ')	
full_songs = full_songs.replace('}', ' ')
full_songs = full_songs.replace(']', ' ')
full_songs = full_songs.replace('\\r', ' ')
full_songs = full_songs.replace('\\n', ' ')
full_songs = full_songs.replace(' u\'', ' ')
full_songs = full_songs.replace(' u\"', ' ')
full_songs = full_songs.replace('\".', ' ')
full_songs = full_songs.replace('\',', ' ')
full_songs = full_songs.replace('\'.', ' ')
full_songs = full_songs.replace('\",', ' ')
full_songs = full_songs.replace('\"', ' ')
full_songs = full_songs.replace('.', ' ')
full_songs = full_songs.replace(',', ' ')
full_songs = full_songs.replace('\'lyrics\':', ' ') 
full_songs = full_songs.replace('\\u2019', "\'" )

songTokenized = nltk.word_tokenize(full_songs) 						#woorden tokenizen

songPosTagged = nltk.pos_tag(songTokenized)					#woorden pos taggen
songPosTaggedContent = []

for row in range(len(songPosTagged)):							#als een woord een bepaalde POS is, heeft het inhoud, dus moet het in de lijst
#	if songPosTagged[row][1] == 'JJ':
#		songPosTaggedContent.append(songPosTagged[row][0])
#	elif songPosTagged[row][1] == 'JJR':
#		songPosTaggedContent.append(songPosTagged[row][0])
#	elif songPosTagged[row][1] == 'JJS':
#		songPosTaggedContent.append(songPosTagged[row][0])
#	misschien nog de adjectives plakken aan nouns
	if songPosTagged[row][1] == 'NN':
		songPosTaggedContent.append(songPosTagged[row][0])
	elif songPosTagged[row][1] == 'NNS':
		songPosTaggedContent.append(songPosTagged[row][0])
	elif songPosTagged[row][1] == 'NNP':
		songPosTaggedContent.append(songPosTagged[row][0])
	elif songPosTagged[row][1] == 'NNPS':
		songPosTaggedContent.append(songPosTagged[row][0])	

songFreqDist = nltk.FreqDist(songPosTaggedContent)								#frequentie van woorden
songMostCommonWords = songFreqDist.most_common(len(songFreqDist))					#een lijst van meest voorkomende woorden

crapWords = ['na', 'oh', 'em', 'ehm', 'oeeeh', 'ai', 'ay', 'ette', 'come', 'oeh', 'way', 'chorus', 'bah', 'ba', 'ah-ha', 'cause', 'verse', 'mmm', 'let', 'yo', 'go', 'da', 'ta', 'aye', 'yeah', 'la', 'da-da' 'ta', 'get', 'ooh', 'jah', ')', '(', 'gon', 'wan', 'eh', 'ya', 'i', artist_name.lower(), 'ah', 'cuz', 'hey', 'j', 'woah' , 'oooh','uh']		#woorden die niets over de inhoud van de text zeggen
stopWords = stopwords.words('english')

i=0
lengthSongMostCommonWords = len(songMostCommonWords)
while i < lengthSongMostCommonWords:													#voor elk element uit de lijst van de meest voorkomende woorden
	for j in range(len(crapWords)):												#kijk door de hele stopwoordenlijst
		if crapWords[j] == songMostCommonWords[i][0]:								#als het element uit de lijst van meest voorkomende woorden in de stopwoordenlijst zit
			songMostCommonWords.remove(songMostCommonWords[i])							#verwijder het dan uit de lijst van meest voorkomende woorden
			lengthSongMostCommonWords -= 1;											#pas de lengte aan, zodat de index niet out of range raakt
			i -= 1 																#de index moet op zijn plek blijven, omdat er een item uit de lijst is verwijderd en de indexen zijn verschoven
			break	
	for k in range(len(stopWords)):												#kijk door de hele stopwoordenlijst
		if stopWords[k] == songMostCommonWords[i][0]:								#als het element uit de lijst van meest voorkomende woorden in de stopwoordenlijst zit
			songMostCommonWords.remove(songMostCommonWords[i])							#verwijder het dan uit de lijst van meest voorkomende woorden
			lengthSongMostCommonWords -= 1;											#pas de lengte aan, zodat de index niet out of range raakt
			i -= 1 															#de index moet op zijn plek blijven, omdat er een item uit de lijst is verwijderd en de indexen zijn verschoven
			break																			#het doorzoeken van de stopwoordenlijst is niet meer nodig
	i += 1																		#het volgende element

resultTopics = []

f = open('results.txt', 'w')
for i in range(10):
	f.write(songMostCommonWords[i][0] + '\n')
	resultTopics.append(songMostCommonWords[i][0])

def imageUrlFind(keyword, maxImages,startCount):
    masterLinks=list()
    imageCount = startCount
    endFlag = 0
    try:
        while imageCount < maxImages and endFlag is 0:
            imageCount = imageCount + 20
            url = """https://www.flickr.com/search/?q=%s""" % ((keyword.replace(' ', '+')))
            opener = urllib2.build_opener()
            request = urllib2.Request(url)
            request.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.2.10) Gecko/20100914 Firefox/3.6.10 ( .NET CLR 3.5.30729)')
            data = opener.open(request).read()
            soup = BeautifulSoup(data)
            links = soup.findAll('img')
            strLink= list()
            for link in links:
                strLink.append(str(link))
            endFlag = 1
            for link in strLink:
            	regex = re.findall('data-defer-src="(.*).jpg" ', link)
                if regex != []:
                    if len(masterLinks) < maxImages:    
                        link = regex[0] + '.jpg'
                        masterLinks.append(link)
                        endFlag = 0
        return masterLinks
    except:
        return masterLinks

def ensure_dir(d):
    if not os.path.exists(d):
        os.makedirs(d)

counter = 0
def downloadImages(links, folderName, startNumber):
    global counter, downloading_images
    if counter == 0:
        ensure_dir('images/%s' % folderName)
        os.chdir('images/%s' % folderName)
    elif counter > 0:
        ensure_dir('../%s' % folderName)
        os.chdir('../%s' % folderName)

    imageNumber = startNumber
    for link in links:
        try:
            imageNumber = imageNumber + 1
            image = urllib.URLopener()
            image.retrieve(link,str(imageNumber) + re.findall('(\.jpg+|\.png+|\.gif)',link)[0])
        except:
            yoiu = 2
    return imageNumber

def retrieveImage(resultTopic, importance):
	links = imageUrlFind(resultTopic, 5, 0)
	numberImagesDownloaded = downloadImages(links,importance, startNumber)

startNumber = 0
artistName = artist_name
retrieveImage(artistName, 'artist')

for i in range(len(resultTopics)):
	counter += 1
	retrieveImage(resultTopics[i], i)

# processing songs (cleaning the files: getting rid of unwanted tokens)
songs = []
for song in songtext:
	songs += song['lyrics']

# cleaning per line
songs_cleaned = []
for line in songs:
	line = line.lower()
	line = line.replace('\r\n', '')
	line = line.replace('\r', '')
	line = line.replace('\n', '')
	line = line.replace('u\"', '')
	line = line.replace('\".', '')
	line = line.replace('\',', '')
	line = line.replace('\'.', '')
	line = line.replace('\",', '')
	line = line.replace('.', '')
	line = line.replace(',', '')
	line = line.replace("']}]", '')
	songs_cleaned.append(line)

# dictionary tagger
dict_tagged_sentences = []
score = 0

# tag the songs
for i in songs_cleaned:
	pos_tag = sentiment_analysis.tokenize_songtext(i)
	dic_tag = dicttagger.tag(pos_tag)
	dict_tagged_sentences += [dic_tag]

# calculate sentiment analysis score
for i in dict_tagged_sentences:
	score += sentiment_analysis.sentiment_score(i)

# calculate the percentage positive/negative out of the amount of words classified either positively or negatively
words_total = float(sentiment_analysis.words_total)
words_positive = float(sentiment_analysis.words_positive)
words_negative = float(sentiment_analysis.words_negative)

percentage_positive = words_positive / words_total
percentage_negative = words_negative / words_total

score_to_print_positive = int(percentage_positive * 100)
score_to_print_negative = int(percentage_negative * 100)

sentiment_score_file = open("../../sentiment_score_file.txt", 'w')
sentiment_score_file.write(str(score_to_print_positive))


# HTML MAGIC

print "<p>The results of the sentiment analysis of %s are: %s percent of classified words was positive, and %s percent of the words was negative.</p>" % (artist_name, score_to_print_positive, score_to_print_negative)
print "<br>"
print "<p>The main topics of <b>%s</b> are: %s, %s, %s, %s, %s, %s, %s, %s, %s</p>" % (artist_name, resultTopics[0], resultTopics[1], resultTopics[2], resultTopics[3], resultTopics[4], resultTopics[5], resultTopics[6], resultTopics[7], resultTopics[8])

print "<a class=\"btn btn-default\" href=\"make_moodboard\" role=\"button\">Go to the Moodboard!</a>"
print "</div>"
print "</div>"
print "</div>"




