#!/usr/bin/env python3
# Written by Rhythm Lunatic

import sys
import os
import subprocess
import inquirer
import requests
import json
#import urllib.parse

if not os.path.isfile("key.txt"):
	print("Please put your YouTube API key in a file named key.txt and restart.")
	sys.exit(0)
api_key = None
with open("key.txt","r") as f:
	api_key = f.read().strip()

query = input("Search for a video...")
params = {'part':'snippet','type':'video','key':api_key,'q':query}
response = requests.get("https://youtube.googleapis.com/youtube/v3/search",params=params)
j = json.loads(response.text)

choices = [i['snippet']['title'] for i in j['items']]
prompt = [
	inquirer.List("video",
		message="Pick the first song to play.",
		choices=choices
	)
]
promptResult = inquirer.prompt(prompt)
if promptResult == None:
	sys.exit(0)

def findYTVideoIdFromInquirerResults(string):
	for v in j['items']:
		if v['snippet']['title'] in string:
			return v['id']['videoId']
			
vidID = findYTVideoIdFromInquirerResults(promptResult['video'])
print(vidID)

AlreadyPlayedVideos = []

while True:
	#Remove previous video or ytdl won't download it
	if os.path.isfile("out"):
		os.remove('out')
	try:
		subprocess.check_call(['youtube-dl', '-f bestaudio','-o','out',"https://www.youtube.com/watch?v="+ vidID],stderr=subprocess.STDOUT)
		subprocess.call(['mplayer',os.path.join(os.getcwd(),'out')])
	except subprocess.CalledProcessError as err:
		print(err)
		print("This video can't be played... Trying the next one.")
		#sys.exit(-1)
	AlreadyPlayedVideos.append(vidID)

	params={'part':'snippet','type':'video','relatedToVideoId':vidID,'key':api_key}
	response = requests.get("https://youtube.googleapis.com/youtube/v3/search",params=params)
	#print(response.text)
	
	for video in json.loads(response.text)['items']:
		if video['id']['videoId'] not in AlreadyPlayedVideos:
			vidID = video['id']['videoId']
			break
	
	#url = "https://www.youtube.com/watch?v="+ vidID
