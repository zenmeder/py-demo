#coding=utf-8
import urllib.request as urlrq
import re

def getHtml(url):
	page=urlrq.urlopen(url)
	pageInfo=page.read()
	return str(pageInfo)
def getTeams(info):
	regx='<strong class=\"jqjq\">(\w*)<\/strong>'
	pattern=re.compile(regx)
	ma=pattern.findall(info)
	return ma
def getTime(info):
	# regx='<p>(\d{4}-\d{2}-d{2})\s*(\d{2}:\d{2})<\p>'
	regx='<p>(2017.*?)</p>'
	pattern=re.compile(regx)
	ma=pattern.findall(info)
	return ma
url='http://www.wanplus.com/schedule/22713.html'

info=getHtml(url)
print(getTeams(info))
print(getTime(info))

