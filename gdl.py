from lxml import html
from urlparse import urlparse, parse_qs
from tomorrow import threads
import requests, os, re

def extract_urls(fp):
	a = fp.read()
	b = html.fromstring(a)
	urls = b.xpath('//a[@class="rg_l"]/@href')
	urls = [parse_qs(urlparse(url).query)['imgurl'][0] for url in urls]
	return urls

def download(url):
	header = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:32.0) Gecko/20100101 Firefox/32.0',}
	return requests.get(url, stream=True, headers=header)

def async_download(urls, path):
	if not os.path.exists(path):
		os.makedirs(path)

	for i, url in enumerate(urls):
		r = download(url)
		title = url.split('/')[-1]
		with open(os.path.join(path, str(i) + '_' + title), 'wb') as fp:
			for block in r.iter_content(1024):
				fp.write(block)

	with open(os.path.join(path, 'urls.txt'), 'w') as fp:
		fp.write('\n'.join([str(i) + ' ' + url for i, url in enumerate(urls)]))

with open('line.html', 'r') as fp: # Use your own html of google image search page
	urls = extract_urls(fp)

async_download(urls, 'linechart')