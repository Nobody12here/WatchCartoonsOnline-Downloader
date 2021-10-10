from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import asyncio
from arsenic import get_session,keys,browsers,services

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
	EpisodeLinks = []
	page = requests.get(url)
	soup = BeautifulSoup(page.content,"html.parser")
	container = soup.find_all("div",class_="cat-eps")
	for link in container:
		
		EpisodeLinks.append(link.a["href"])
	return EpisodeLinks

async def getVideoFrameLink(ListOfLinks):
	'''
	Uses seleinum in headless mode to
	get the iframe source link from the episode link.
	You need to pass the episode links as a list
	Note:Besure that you have the chrome driver installed and set up
	in your PATH 
	'''
	VideoFrameLinks = []
	service= services.Chromedriver(binary="chromedriver")
	browser = browsers.Chrome()

	browser.capabilities = {
	"goog:chromeOptions":{"args":["--disable-gpu", "--no-sandbox", "--disable-dev-shm-usage"]}
	}
	async with get_session(service, browser) as session:
		for url in ListOfLinks:
			await session.get(url)
			try:
				iframeEL = await session.get_element("#cizgi-js-0")
			except:
				print("somthings wrong with ",url)
				print("-------------------")
				iframeEL = await session.get_element("#anime-js-0")
			iframe = "https://www.wcoforever.net" + await iframeEL.get_attribute("src")
			VideoFrameLinks.append(iframe)
	return VideoFrameLinks

def getVideoLink(ListOfLinks):
	'''
	Gets the video link from the list of iframe links
	Uses seleinium to get the video link
	Note:Use seleinium without --headless arg to get the link
	Otherwise it will not work.Don't ask Don't know :)
	'''
	VideoLink =[]
	for link in ListOfLinks:
		driver = webdriver.Chrome()
		driver.get(link)
		html = driver.page_source
		driver.quit()
		soup = BeautifulSoup(html,"html.parser")
		Link = soup.find("video",id = "video-js_html5_api")
		VideoLink.append(Link["src"])
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
	loop = asyncio.get_event_loop()
	EpL = getEpisodesLink(url)
	VideoFrame = loop.run_until_complete(getVideoFrameLink(EpL))
	VideoLink = getVideoLink(VideoFrame)
	print(VideoLink)

if __name__ == '__main__':
	main("https://www.wcofun.com/anime/rick-and-morty")