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

@threads(5)
def download(url):
	header = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:32.0) Gecko/20100101 Firefox/32.0',}
	return requests.get(url, stream=True, headers=header)

# Gevent is somehow crashing due to python 2.7.10 ssl issue
# So this is NOT async version!
def async_download(urls, path):
	if not os.path.exists(path):
		os.makedirs(path)

	for i, url in enumerate(urls):
		print i, url
		r = download(url)
		title = url.split('/')[-1]
		with open(os.path.join(path, str(i) + '_' + title), 'wb') as fp:
			for block in r.iter_content(1024):
				fp.write(block)

	with open(os.path.join(path, 'urls.txt'), 'w') as fp:
		fp.write('\n'.join([str(i) + ' ' + url for i, url in enumerate(urls)]))

qs = ['area', 'bar', 'line', 'map', 'pareto', 'pie', 'radar', 'scatter', 'table', 'venn']

for q in qs:
	with open(os.path.join('resource', q + '.html'), 'r') as fp: # Use your own html of google image search page
		urls = extract_urls(fp)
	async_download(urls, q)