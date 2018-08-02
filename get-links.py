from BeautifulSoup import BeautifulSoup
import urllib2
import re
import sys

page_link = str(sys.argv[1])

#"http://oceans11.lanl.gov/deepwaterimpact/yB11_300x300x300-FourScalars_resolution.html"

def getLinks(url):
    html_page = urllib2.urlopen(url)
    soup = BeautifulSoup(html_page)
    links = []

    for link in soup.findAll('a', attrs={'href': re.compile("^http://.*\.vti$")}):
        links.append(link.get('href'))

    return links


for link in getLinks(page_link):
    print link

#cat urlfile | parallel --gnu "wget {}"
