from HTMLParser import HTMLParser
from htmlentitydefs import name2codepoint
import urllib2
import re
import string
import os.path
import subprocess
from time import strftime, gmtime
import time





# VVVVVVVVVVVVVVVVVVVVV

# Only works on Windows.

# /\ /\ /\ /\ /\ /\ /\ 





#############################################
#############################################
#############################################
############## Edit Stuff Here ##############
#############################################
#############################################
#############################################

#insert first couple of words of group+show you want
# Eg, what do you enter in the search terms

listOfAnimes = []*6
listOfAnimes[0] = "hatsuyuki unlimited blade 10bit"
listOfAnimes[1] = "chihiro grisaia no"
listOfAnimes[2] = "ore twintail ni narimasu commie"
listOfAnimes[3] = "inou battle wa nichijou commie"
listOfAnimes[4] = "trinity seven damedesuyo"
listOfAnimes[5] = "vivid amagi brilliant park"
listOfAnimes[6] = ""


#Root directory for shows
baseDirectory = "D:\\Anime Torrents\\"

#Folder names in said root directory
folderNames = []*6
folderNames[0] = "Fate Stay Night - Ufotable"
folderNames[1] = "Grisaia no Kajitsu"
folderNames[2] = "Ore, Twintail ni Narimasu"
folderNames[3] = "Inou Battle wa Nichijou-kei no Naka de"
folderNames[4] = "Trinity Seven"
folderNames[5] = ""
folderNames[6] = ""

#Path to BitTorrent
bittorrentPath = r'G:\\BitTorrent\\BitTorrent.exe'


#############################################
#############################################
#############################################
############ Don't Edit Past Here ###########
#############################################
#############################################
#############################################





url = []*6
for i in xrange(len(listOfAnimes)):
	returnString = ""
	for c in listOfAnimes[i]:
		if c in string.ascii_letters or c == " ":
			returnString+=c.lower()
	url[i] = returnString


for i in range(len(listOfAnimes)):
	listOfAnimes[i] = string.replace(listOfAnimes[i],"[","\[")
	listOfAnimes[i] = string.replace(listOfAnimes[i],"]","\]")	
	print listOfAnimes[i]

dataArray = ["", "", ""]

for i in range(len(url)):
	if url[i] != "Blank!":
		temp = url[i].split(" ")
		url[i] = "http://www.nyaa.se/?page=search&cats=0_0&filter=0&term="
		for x in range(len(temp)):
			url[i] = url[i]+temp[x]
			if x != len(temp)-1:
				url[i] = url[i]+"+"
	print url[i]

	
def doesExist(torrentLoc):
	if os.path.isfile(torrentLoc) == True:
		return True
	if os.path.isfile(torrentLoc) == False:
		return False

def openTorrent(torrentLoc, animeLoc, data):
	subprocess.call([bittorrentPath, "/directory", animeLoc, torrentLoc])
	print "@@@@@@@@@@@@@@"
	print "@@@Success!@@@"
	print "@@@@@@@@@@@@@@"
	print "Downloading", data, "to", animeLoc+data
	
class NyaaParser(HTMLParser):
	def handle_starttag(self, tag, attrs):
		#print "Start tag: ", tag
		for attr in attrs:
			#print "--attr:", attr
			if tag == 'a' and re.match("\('href',", str(attr)) != None:
				attribute = str(attr)
				dataArray[0] = attribute[11:-2]
				dataArray[0] = string.replace(dataArray[0],"view","download")
	def handle_data(self, data):
		for i in xrange(len(listOfAnimes)):
			torrentLoc = baseDirectory+"\\"+folderNames[i]+"\\"+"torrents\\"+data+".torrent"
			if re.match(i, str(data)) != None and re.search(".mkv", str(data)) != None:
				print "Torrent Name: ", data
				print "Match found!"	
				if doesExist(torrentLoc) == False:
					print "!!!!!!Downloading file!!!!!!"
					print "Downloaded to: "+torrentLoc
					urlFile = urllib2.urlopen(dataArray[0]+"&txt=1")
					print "Torrent downloaded from: "+dataArray[0]+"&txt=1"
					localFile = open(torrentLoc, 'wb')
					localFile.write(urlFile.read())
					localFile.close()
					animeLoc = string.replace(torrentLoc,"\\torrents\\"+data+".torrent","")
					if doesExist(animeLoc+data) == False:
						openTorrent(torrentLoc, animeLoc, data)
					else:
						print "Weird. Seems like you didn't have the torrent file but DID have the mkv file already! Bittorrent not opened."
					print "------------------------------------"
					print "------------------------------------"				
				else:
					print "Oops! Already exists on local drive. Not downloading", data + ".torrent"
					print "------------------------------------"
					print "------------------------------------"
		

lastTime = ""
while 1:
	if strftime("%H:%M:%S", gmtime()) == "03:59:59":
		for i in url:
			if i != "":
				print i
				data = urllib2.urlopen(i)
				source = data.read()
				parser = NyaaParser()
				parser.feed(source)
				print "&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&"
			else:
				print "No more animes to search! We're done!"
				break
	else:
		if lastTime != strftime("%H:%M:%S", gmtime()):
			print "Will check for new episodes at 03:59:59PM UTC. Current time is: "+strftime("%H:%M:%S", gmtime()), "UTC"
		lastTime = strftime("%H:%M:%S", gmtime())
		time.sleep(0.1)


