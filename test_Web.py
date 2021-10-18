from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
SeasonLink = "https://www.wcofun.com/anime/family-guy-season-7" #You can change that to whatever season
def search(name):
	'''
	searches the desired cartoon in the website
	Enter the name of the cartoon and you will get the link to its seasons in a list form

	'''
	link=""
	website = "https://www.wcofun.com/search"
	driver = webdriver.Chrome()
	driver.get(website)
	searchBar = driver.find_element_by_class_name("catara2")
	searchBar.send_keys(name)
	searchBar.send_keys(Keys.ENTER)
	content = driver.find_elements_by_css_selector(".recent-release-episodes a")
	for href in content:
		link = href.get_property("href")
	return link

def getEpisodesLink(url):
	'''
	This function takes in a link of Season of Show the family guy
	and returns the list of links of episode in that season
	'''
	page = requests.get(url)
	soup = BeautifulSoup(page.content,"html.parser")
	container = soup.find_all("div",class_="cat-eps")
	EpisodeLinks = [link.a["href"] for link in container]
	return EpisodeLinks

def getVideoLink(ListOfLinks):
	'''
	Gets the video link from the list of iframe links
	Uses seleinium to get the video link
	Note:Use seleinium without --headless arg to get the link
	Otherwise it will not work.Don't ask Don't know :)
	'''

	VideoLink =[]
	driver = webdriver.Chrome(options=chrome_options)
	wait = WebDriverWait(driver, 30)
	for url in ListOfLinks:
		driver.get(url)
		try:
			iframe = wait.until(EC.presence_of_element_located((By.XPATH,"//*[@id='cizgi-js-0']")))
			driver.switch_to.frame(iframe)
		except:
			print("Some error occured in the link ",url)
			
		link = ( driver.find_element("tag name","video").get_attribute("src") )
		print(link)
		VideoLink.append(link)
		
	driver.quit()
	return VideoLink

def DownloadVideos(ListOfLinks):
	agents = {"user-agent":"Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36"}
	for link in ListOfLinks:

		FileContent = requests.get(link,stream=True,headers=agents)
		print(FileContent.headers)
		print("Downloading Started")
		with open("familyGuyS7"+".mp4",'wb') as downloadFile:
			downloadFile.write(FileContent.content)
		print("Finished Downloading")

def main(url):
	
	EpL = getEpisodesLink(url)
	
	VideoLink = getVideoLink(EpL)
	print(VideoLink)
if __name__ == '__main__':
	main("https://www.wcofun.com/anime/rick-and-morty")