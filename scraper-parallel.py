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
start_url = 'https://en.wikipedia.org/wiki/Special:Random'
# use random page as start
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
	if url[:24] == 'https://en.wikipedia.org' and all(s not in set(url[24:]) for s in ':#?'):
		return True
	else:
		return False


W = 8 # total workers
C = 0  # just a counter
T = 50 # amount of work ( # of pages )
N = 30 # maximum fork from each page
F = 1048576 # about 1 mb


for _ in range(W):
	url_queue.put(start_url)
url_set.add(start_url)

set_lock = threading.Lock()
dir_lock = threading.Lock()

def task(I, C, T):
	options = webdriver.ChromeOptions()
	options.add_argument('--headless')
	browser = webdriver.Chrome(service = Service(ChromeDriverManager().install()), options=options)

	dir_lock.acquire()
	output_file = open(randomPathInResultDir(16), 'w', encoding='utf-8')
	dir_lock.release()
	file_length = 0 # record written bytes

	while not url_queue.empty() and C < T:
		
		target_url = url_queue.get()

		pgr = file_length / F * 100
		print(f'Thread({I:2}) progress: [{C:4}/{T:4}] file_cap: {pgr:7.3f}% url: {target_url}')
		
		try:
			browser.get(target_url)
		except:
			print('Some how fail to open url')
			continue

		# retrieve text

		texts = browser.find_elements(By.XPATH, "//div[@id='mw-content-text']//p")

		for text in texts:
			try:
				output_file.write(text.text)
				file_length += len(text.text)
			except:
				print('Cannot get the text of page element')
				continue
			# refresh file if it is too large
			if file_length >= F:
				output_file.flush()
				output_file.close()
				dir_lock.acquire()
				output_file = open(randomPathInResultDir(16), 'w', encoding='utf-8')
				dir_lock.release()
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

	browser.close()


handles = [threading.Thread(target=task, args=(i+1, C, T,)) for i in range(W)]


for (i, handle) in enumerate(handles):
	handle.start()
	print(f'Thread {i} is started.')

for (i, handle) in enumerate(handles):
	handle.join()
	print(f'Thread {i} is joined.')