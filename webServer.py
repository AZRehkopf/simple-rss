import cherrypy, dominate, json, os, os.path
from dominate.tags import *


path   = os.path.abspath(os.path.dirname(__file__))
config = {
  'global' : {
    'server.socket_host' : '127.0.0.1',
    'server.socket_port' : 8080,
    'server.thread_pool' : 8
  },
  '/css' : {
    'tools.staticdir.on'  : True,
    'tools.staticdir.dir' : os.path.join(path, 'css')
  }
}

class feedDisplay(object):
    @cherrypy.expose
    def index(self):
        with open('/Users/atlas/Documents/Programming/Python/rssParser/cache/spacex', 'r') as fp:
          feed = json.load(fp)

        doc = dominate.document(title='Feeds')
        with doc.head:
            link(rel='stylesheet', href='/css/style.css')
            link(rel='stylesheet', href='https://fonts.googleapis.com/css?family=Roboto:100')

        with doc:
            with div(id='header').add(ul()):
                for i in feed:
                    li(a(feed[i]['title'], href=feed[i]['link']))
        return str(doc)

if __name__ == '__main__':
    
    cherrypy.quickstart(feedDisplay(), '/', config)