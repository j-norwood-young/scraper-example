from bs4 import BeautifulSoup
import urllib2
import re
import csv

def get_a_dude(wid):
	response = {}
	html = urllib2.urlopen("http://www.saps.gov.za/crimestop/wanted/"+wid).read()
	dudepage = BeautifulSoup(html)

	top_table = dudepage.table
	info_table = top_table.contents[7].table

	name = info_table.h2.string
	response["name"] = name

	details_table = info_table.table

	image = details_table.img

	response["image"]="http://www.saps.gov.za/crimestop/wanted/" + image["src"]

	for field in details_table.find_all(text=re.compile("\:")):
		response[field.replace(": ", "")] = field.parent.parent.next_sibling.string

	return response

murder_url = "http://www.saps.gov.za/crimestop/wanted/detailcrimecat.php?cid=44"

html = urllib2.urlopen("http://www.saps.gov.za/crimestop/wanted/detailcrimecat.php?cid=44").read()
murder_page = BeautifulSoup(html)

murder_lines = murder_page.find_all(href=re.compile("wid"))
urls = []
for item in murder_lines:
	if (not item["href"] in urls):
		urls.append(item["href"])

dudes = []

for url in urls:
	dudes.append(get_a_dude(url))

s = ""
for key in dudes[0]:
	s = s + key+","
print s

for dude in dudes:
	s = ""
	for key in dudes[0]:
		s = s + dude[key]+","
	print s