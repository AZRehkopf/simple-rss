import feedparser, ssl, os, json, pytz
import datetime as dt
from dateutil import parser

RSS_PATH = '/Users/atlas/Documents/Programming/Python/rssParser'

# Connects and fetches the RSS feed and returns the parsed data
def connectAndParseFeed(target):
        if hasattr(ssl, '_create_unverified_context'):
            ssl._create_default_https_context = ssl._create_unverified_context

        return feedparser.parse(target)

# Creates necessary folders for program operation
def initailizeFileStructure(path):
        if not os.path.exists(path):
                os.makedirs(path)
        if not os.path.exists(path + '/cache'):
                os.makedirs(path + '/cache')

# Saves relevant info in the feed as JSON
def createJsonAndCache(target, path):
        feed_name = getFeedName(target)
        cache_path = path + '/cache/' + feed_name
        data = collectData(target)

        if not os.path.isfile(cache_path):
                with open(cache_path, 'w') as fp:
                        json.dump(data, fp, sort_keys = True, indent = 4)
        else:
                with open(cache_path, 'r') as fp:
                        cache = json.load(fp)
                        merged = cache.copy()
                        merged.update(data)

                merged = checkForNew(merged)

                with open(cache_path, 'w') as fp:
                        json.dump(merged, fp, sort_keys = True, indent = 4)               

# Collects all the relevant info from the feed and returns as a dict
def collectData(target):
        titles = []
        timestamps = []
        links = []
        new = []
        data = {}
        feed = connectAndParseFeed(target)

        for articles in feed['items']:
                titles.append(articles['title'])
                try: 
                    timestamps.append(str(parser.parse(articles['published'])))
                except KeyError:
                    timestamps.append(str(parser.parse(articles['date'])))
                links.append(articles['link'])
                new.append(False)
                
        for num in range(len(titles)):
                data.update({timestamps[num]:{'title': titles[num], 'link': links[num], 'new':new[num]}})
        return data

# Returns the feed name as a string
def getFeedName(target):
        feed = connectAndParseFeed(target)
        try:
            return feed['feed']['tags'][0]['term']
        except KeyError:
            return feed['feed']['title']

# Logs the time that the feed was accessed
def logTime(path):
        log_path = path + '/log'
        if not os.path.isfile(log_path):
                log = {'accessed':str(dt.datetime.utcnow())}
                with open(log_path, 'w') as fp:
                        json.dump(log, fp, sort_keys = True, indent = 4)
        else:
            with open(log_path, 'r') as fp:
                    log = json.load(fp)
                    log.update({'accessed':str(dt.datetime.utcnow())})
            with open(log_path, 'w') as fp:
                    json.dump(log, fp, sort_keys = True, indent = 4)

# Returns time of the last feed access
def getLastAccess(path):
        path = path + '/log'

        if not os.path.isfile(path):
                return None
        else:
                with open(path, 'r') as fp:
                        log = json.load(fp)
                try: 
                        return log['accessed']
                except KeyError:
                        return None

# Checks if a post is in memory if it is, 'new' is set to true
def checkForNew(data):
    for item in data:
        item_time = parser.parse(item) 
        if (pytz.utc.localize(dt.datetime.utcnow()) - item_time) < dt.timedelta(hours = 3):
            data[item]['new'] = True
    return data

# Fetches URLs to be scaned
def getFeedUrls(path):
    path = path + '/log'
    with open(path, 'r') as fp:
        log = json.load(fp)
    try:
        return log['URLs']
    except KeyError:
        return None   

# Updates all feed cache files 
def updateFeeds():
    initailizeFileStructure(RSS_PATH)
    feeds = getFeedUrls(RSS_PATH)

    for url in feeds:
        createJsonAndCache(url, RSS_PATH)
        print('Fetching ' + url + '...')
	
    logTime(RSS_PATH)
    mergeFeeds(RSS_PATH)

# Merges all individual feeds into one single file 
def mergeFeeds(path):
	all_data = {}
	for file in os.listdir(path + '/cache'):
		if not file.startswith('.'):
			with open(path + '/cache/' + file, 'r') as fp:
				all_data.update(json.load(fp))
			with open(path + '/feeds', 'w') as fp:
				json.dump(all_data, fp, sort_keys = True, indent = 4)

if __name__ == '__main__':			
	updateFeeds()
