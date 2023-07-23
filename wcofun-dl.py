#!/usr/bin/python3

# Original script by Nobody12here
# https://github.com/Nobody12here/WatchCartoonsOnline-Downloader
#
# Code updated by Timmy Ramone
# Works on wcofun.com as of 11/2022
#
# wcofun-dl.py --url URL 
#
# Replace URL with homepage of the series you want to download, e.g.:
# wcofun-dl.py --url https://www.wcofun.com/anime/teen-titans-go

from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import argparse
import time
import sys
import os

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument(f'user-agent={"Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36"}')
#chrome_options.add_argument("--window-size=1920,1200")

def getEpisodesLink(url):
	'''
	This function takes in a link of Season of Show url
	and returns the list of links of episodes in that season
	'''

	print("Getting episode titles/links...")
	driver = webdriver.Chrome(options=chrome_options)
	wait = WebDriverWait(driver, 30)
	driver.get(url)
	try:
		wait.until(EC.presence_of_element_located((By.XPATH,"//*[@class='cat-eps']")))
	except:
		print("\nERROR: Unable extract episode list from", url)
		sys.exit(1)

	#print(driver.page_source)
	#page = requests.get(url)
	#soup = BeautifulSoup(page.content,"html.parser")
	soup = BeautifulSoup(driver.page_source,"html.parser")
	container = soup.find_all("div",class_="cat-eps")
	EpisodeLinks = [link.a["href"] for link in container]

	return EpisodeLinks

def getVideoLink(ListOfLinks):
	'''
	Gets the video link from the list of iframe links
	Uses seleinium to get the video link
	Note: Use seleinium without '--headless' arg for debugging
	Note: --headless mode will work but only if you set the proper
		user-agent (see above) -TR
	'''

	print("Downloading Episodes...\n")

	VideoLink =[]
	driver = webdriver.Chrome(options=chrome_options)
	wait = WebDriverWait(driver, 60)
	#wait = WebDriverWait(driver, 15)

	for url in ListOfLinks:
		myFile = os.path.basename(url) + ".mp4"
		print("Download File: "+myFile)

		if  (os.path.exists(myFile)):
			print("File exists -- skipping...\n")
		else:
			driver.get(url)
			#time.sleep(5)
			try:
				iframe = wait.until(EC.presence_of_element_located((By.XPATH,
					"//*[@id='cizgi-js-0']")))
				driver.switch_to.frame(iframe)
				time.sleep(1)
			except:
				print("Some error occured in the link ",url)
				sys.exit(1)
			
			link = ( driver.find_element("tag name","video").get_attribute("src") )
			VideoLink.append(link)
			DLVideos(myFile, link)
			#driver.quit() DONT USE THIS!
			time.sleep(1)

	return VideoLink

def DLVideos(myFile, link):
	agents = {"user-agent":"Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36"}

	FileContent = requests.get(link, stream=True, headers=agents)
	#print(FileContent.headers)
	print("Downloading...")
	with open(myFile, 'wb') as downloadFile:
		downloadFile.write(FileContent.content)
	print("Finished Downloading\n")

def main(url):
	
	EpL = []
	EpL = getEpisodesLink(url)
	
	#kludge-code for testing
	#EpL=["https://www.wcofun.net/t-u-f-f-puppy-season-3-episode-8-puff-puppy-stressed-to-kill"]
	#EpL.append("https://www.wcofun.net/t-u-f-f-puppy-season-3-episode-7-while-the-cats-away-sweet-revenge")
	#print("EpL:")
	#print(EpL)

	VideoLink = getVideoLink(EpL)
	#print(VideoLink)

	print("DONE.")

if __name__ == '__main__':

	# Initialize commandline options
	parser = argparse.ArgumentParser(
		# prog = "wcofun-dl.py",
		# description="Test command line input.",
		epilog = '')
	parser.add_argument("-v", "--verbose", help="increase output verbosity",
		action="store_true")
	parser.add_argument("-u", "--url", help="URL of series at wcofun.com (required)")

	# Parse commandline options
	args = parser.parse_args()

	if args.url:
		if args.verbose:
			print("url="+args.url)
		main(args.url)
	else:
		print("\nNeed a valid URL to start, e.g.:")
		print(sys.argv[0] + " --url https://wcofun.com/myseries\n")

