from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from queue import Queue
from random import shuffle, choices
from os.path import exists
from os import mkdir

import threading

# shared among workers
url_queue = Queue()
url_set = set() # this use async/await
start_url = 'https://en.wikipedia.org/wiki/Main_Page'
result_dir = './scraped_data'

if not exists(result_dir):
	mkdir(result_dir)

def randomPathInResultDir(length):
	
	while True:
		s = ''.join(choices('123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz', k=length))
		p = f'{result_dir}/{s}.data'
		if not exists(p):
			break
	return p

def checkUrl(url):
	global url_set
	if not isinstance(url, str):
		return False
	if url in url_set:
		return False
	if len(url) <= 24:
		return False
	if url[:24] == 'https://en.wikipedia.org' and ':' not in url[24:]:
		return True
	else:
		return False


W = 5 # total workers
C = 0  # just a counter
T = 10 # amount of work ( # of pages )
N = 30 # maximum fork from each page
F = 16777216


for _ in range(W):
	url_queue.put(start_url)
url_set.add(start_url)

set_lock = threading.Lock()
dir_lock = threading.Lock()

def task(C, T):
	browser = webdriver.Chrome(service = Service(ChromeDriverManager().install()))

	dir_lock.acquire()
	output_file = open(randomPathInResultDir(16), 'w', encoding='utf-8')
	dir_lock.release()
	file_length = 0 # record written bytes

	while not url_queue.empty() and C < T:
		print(f'[{C}/{T}]')
		print(len(url_set))

		target_url = url_queue.get()
		print(f'Now url: {target_url}')

		browser.get(target_url)

		# retrieve text

		texts = browser.find_elements(By.XPATH, "//div[@id='mw-content-text']//p")

		for text in texts:
			output_file.write(text.text)
			file_length += len(text.text)

		# refresh file if it is too large
		if file_length >= F:
			output_file.flush()
			output_file.close()
			output_file = open(randomPathInResultDir(16), 'w', encoding='utf-8')
			file_length = 0
		# find links

		links = browser.find_elements(By.XPATH, "//div[@id='mw-content-text']//a")[:N]
		shuffle(links) # add some randomness

		for link in links:
			new_url = link.get_attribute('href')
			set_lock.acquire()
			if checkUrl(new_url):
				url_set.add(new_url)
				url_queue.put(new_url)
			set_lock.release()
		C += 1

	for url in url_set:
		print(url)

	print(len(url_set))

	browser.close()


handles = [threading.Thread(target=task, args=(C, T,)) for _ in range(W)]


for (i, handle) in enumerate(handles):
	handle.start()
	print(f'Thread {i} is started.')

for (i, handle) in enumerate(handles):
	handle.join()
	print(f'Thread {i} is joined.')