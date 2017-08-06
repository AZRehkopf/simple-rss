import dominate, json, webbrowser
from dominate.tags import *

FILE_PATH = '/Users/atlas/Documents/Programming/Python/rssParser'

def createHtml(path):
	with open(path + '/cache/spacex', 'r') as fp:
	 	feed = json.load(fp)

	doc = dominate.document(title='Feeds')
	with doc.head:
	    link(rel='stylesheet', href='style.css')
	    script(type='text/javascript', src='script.js')

	with doc:
	    with div(id='header').add(ul()):
	        for i in feed:
	            li(a(feed[i]['title'], href=feed[i]['link']))

	with open(path + 'view.html', 'w') as fp:
	 	fp.write(str(doc))

	webbrowser.open('file:///Users/atlas/Documents/Programming/Python/rssParser/view.html')

if __name__ == '__main__':			
	createHtml(FILE_PATH)