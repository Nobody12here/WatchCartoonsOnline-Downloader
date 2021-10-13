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
	driver = webdriver.Chrome()
	for url in ListOfLinks:
		driver = webdriver.Chrome()
		driver.get(url)
		video = driver.find_element_by_class_name("vjs-tech")
		link = video.get_attribute("src")
		print(link)
		VideoLink.append(link)
	driver.close()	
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
	
	# EpL = getEpisodesLink(url)
	# EpL=EpL[0:15]
	# VideoFrame = loop.run_until_complete(getVideoFrameLink(EpL))
	# print(VideoFrame)
	VideoFrame=['https://www.wcoforever.net/inc/embed/video-js.php?file=rick%20and%20morty%2FRick.and.Morty.S05E10.Rickmurai.Jack.1080p.AMZN.WEB-DL.DDP5.1.H.264-NTb.flv&hd=1&pid=551258&h=95b656c14e8d1ab2e6083225686f700d&t=1634100000&embed=ndisk', 'https://www.wcoforever.net/inc/embed/video-js.php?file=rick%20and%20morty%2FRick.and.Morty.S05E09.Forgetting.Sarick.Mortshall.720p.AMZN.WEB-DL.DDP5.1.H.264-NTb.flv&hd=1&pid=551257&h=0b00853a79e54d2b527831f1a619c0d1&t=1634101551&embed=ndisk', 'https://www.wcoforever.net/inc/embed/video-js.php?file=Cartoon%2FRickandMortyS05%2FRick.and.Morty.S05E08.Rickternal.Friendshine.of.the.Spotless.Mort.1080p.AMZN.WEB-DL.DDP5.1.H.264-NTb.flv&hd=1&pid=541182&h=a5ccb09a698b33e4becbe11ffe3ea0a1&t=1634102691&embed=ndisk', 'https://www.wcoforever.net/inc/embed/video-js.php?file=Rick%20and%20Morty%2FSeason%205%2FRick.and.Morty.S05E07.Gotron.Jerrysis.Rickvangelion.1080p.WEB-DL.DDP5.1.x264-NOGRP.flv&hd=1&pid=535570&h=87c63b3af2975c63fc5e12282045a056&t=1634102342&embed=ndisk', 'https://www.wcoforever.net/inc/embed/video-js.php?file=Rick%20and%20Morty%2FSeason%205%2FRick.and.Morty.S05E06.Rick.and.Mortys.Thanksploitation.Spectacular.1080p.AMZN.WEB-DL.DDP5.1.H.264-FLUX.flv&hd=1&pid=535569&h=9c863cae1b635be1df5836d775721cac&t=1634100611&embed=ndisk', 'https://www.wcoforever.net/inc/embed/video-js.php?file=Rick%20and%20Morty%2FSeason%205%2FRick.and.Morty.S05E05.Amortycan.Grickfitti.1080p.AMZN.WEB-DL.DDP5.1.H.264-RICKC137.flv&hd=1&pid=530980&h=b500937c82727ebfd143cdddad4d3460&t=1634102980&embed=ndisk', 'https://www.wcoforever.net/inc/embed/video-js.php?file=Rick%20and%20Morty%2FSeason%205%2FRick.and.Morty.S05E04.Rickdependence.Spray.1080p.AMZN.WEB-DL.DDP5.1.H.264-NOGRP.flv&hd=1&pid=529419&h=b732b84ef1d5cfa9c246738fcab267c9&t=1634100938&embed=ndisk', 'https://www.wcoforever.net/inc/embed/video-js.php?file=Rick%20and%20Morty%2FSeason%205%2FRick.and.Morty.S05E03.A.Rickconvenient.Mort.1080p.AMZN.WEB-DL.DDP5.1.H.264-NTb.flv&hd=1&pid=527763&h=bb1b2e2c3d3b5116f9c84d4cdafc258d&t=1634103021&embed=ndisk', 'https://www.wcoforever.net/inc/embed/video-js.php?file=Rick%20and%20Morty%2FSeason%205%2FRick.and.Morty.S05E02.Mortyplicity.1080p.AMZN.WEB-DL.DDP5.1.H.264-NTb.flv&hd=1&pid=524739&h=c383c8b141440a4295bcccff2c1532d9&t=1634100414&embed=ndisk', 'https://www.wcoforever.net/inc/embed/video-js.php?file=Rick%20and%20Morty%2FSeason%205%2FRick.and.Morty.S05E01.Mort.Dinner.Rick.Andre.1080p.AMZN.WEB-DL.DDP5.1.H.264-NTb.flv&hd=1&pid=521978&h=f744e9e0d6a0659e9d903ad1acb6a3f5&t=1634103232&embed=ndisk', 'https://www.wcoforever.net/inc/embed/video-js.php?file=Cartoon%2FRick%20and%20Morty%20in%20the%20Eternal%20Nightmare%2FWatch%20Rick%20and%20Morty%20in%20the%20Eternal%20Nightmare%20Machine%20Full%20online%20FREE%20-%20KimCartoon.flv&hd=1&pid=507275&h=9439aecc1679785159586c42bf76c098&t=1634100777&embed=ndisk', 'https://www.wcoforever.net/inc/embed/video-js.php?file=Rick%20and%20Morty%2FSeason%204%2FRick.and.Morty.S04E10.Star.Mort.Rickturn.of.the.Jerri.1080p.AMZN.WEB-DL.DD-5.1.H.264-CtrlHD.flv&hd=1&pid=484661&h=4d06c3ea702f7e8010a7fae492ea9d0f&t=1634103663&embed=ndisk', 'https://www.wcoforever.net/inc/embed/video-js.php?file=Rick%20and%20Morty%2FSeason%204%2FRick.and.Morty.S04E09.Childrick.of.Mort.1080p.AMZN.WEB-DL.DD-5.1.H.264-CtrlHD.flv&hd=1&pid=484487&h=3c53d17113d8aed8f49c508b4dd4c360&t=1634101633&embed=ndisk', 'https://www.wcoforever.net/inc/embed/video-js.php?file=Rick%20and%20Morty%2FSeason%204%2FRick.and.Morty.S04E08.The.Vat.of.Acid.Episode.1080p.AMZN.WEB-DL.DD-5.1.H.264-CtrlHD.flv&hd=1&pid=484274&h=a9655000b2e6a983b83ac97a9db883f1&t=1634103320&embed=ndisk', 'https://www.wcoforever.net/inc/embed/video-js.php?file=Rick%20and%20Morty%2FSeason%204%2FRick.and.Morty.S04E07.Promortyus.1080p.AMZN.WEB-DL.DD-5.1.H.264-CtrlHD.flv&hd=1&pid=483975&h=9a1e8fafb156c07e183b76434bc89db6&t=1634101684&embed=ndisk']

	VideoLink = getVideoLink(VideoFrame)
	print(VideoLink)
if __name__ == '__main__':
	main("https://www.wcofun.com/anime/rick-and-morty")