import json, urllib2, weka, os

from bs4 import BeautifulSoup

def ensurePathForFile(filename):
	directory = os.path.dirname(filename)
	if not os.path.isdir(directory):
		print "*Note* Folder '%s' doesn't exist. Creating for file '%s'" %(directory,filename)
		os.makedirs(directory)

def writeJsonToFile(jsonObj, filename, sort_keys_=True):
		f = open(filename, 'w')
		f.write(json.dumps(jsonObj, sort_keys=sort_keys_, indent=4, separators=(',', ': ')))
		f.close()

def loadJsonFromFile(filename):

	f = open(filename)
	ret = json.load(f)

	return ret

def writeHtmlToFile(html, filename):
	f = open(filename, 'w')
	soup = BeautifulSoup(html)
	#if soup.find("AccessTime") == None:
	#	tag = soup.new_tag("AccessTime")
	#	tag.string = self.getDateTimeNow()
	#	soup.body.insert(0, tag)
	f.write(soup.encode('utf-8'))#
	f.close()

def loadHtmlFromFile(self, filename):
	f = open(filename)
	html = f.read().decode('utf-8')
	return html

def readUrl(url):
	return urllib2.urlopen(url).read()

def parse(url, name):
	#
	html = urllib2.urlopen(url).read()
	soup = BeautifulSoup(html)

	headings = [th.text.strip() for th in soup.find("table").find_all('th')]
	rows = [tr.find_all('td') for tr in soup.find("table").find_all('tr')[1:]]

	data = []
	for row in rows:
		datum = {}

		for i in range(0, len(headings)):
			heading =  headings[i]
			value = row[i].text.strip().replace('+','').replace('%', '').replace(" ","-").replace("'","").encode("utf-8")
			value = "0" if len(value)<1 else value

			datum[heading] = value

		data.append(datum)

	'''
	Create ARFF file.
	'''
	arff = weka.Arff()
	arff.setTitle("Final Fantasy XIV - A Realm Reborn | Races/Stats")
	arff.addSource("Creator: Chong-U Lim (culim@mit.edu)")
	arff.addSource("Research Group: Imagination, Computation, and Expression Lab (http://icelab.mit.edu)")
	arff.addSource("Institution: Massachusetts Institute of Technology (http://mit.edu)")
	arff.addSource("FF XIV Guild (http://www.ffxivguild.com/racial-stats-and-god-stats-guide/)")
	arff.setRelation(name)

	heading = headings[0]	# race
	values = [datum[heading] for datum in data]
	attrType = weka.Attribute.TYPE_CLASS
	attr = weka.ClassAttribute(heading, list(set(values)), values)
	arff.addAttribute(attr)

	heading = headings[1]	# sub-race
	values = [datum[heading] for datum in data]
	attrType = weka.Attribute.TYPE_CLASS
	attr = weka.ClassAttribute(heading, list(set(values)), values)
	arff.addAttribute(attr)

	for heading in headings[2:]:
		values = [datum[heading] for datum in data]

		attrType = weka.Attribute.TYPE_NUMERIC if values[0].isdigit() else weka.Attribute.TYPE_STRING
		attr = weka.Attribute(heading, attrType, values)
		arff.addAttribute(attr)



	'''
	Write ARFF.
	'''
	arff_filename = "../arff/%s.arff" %name
	ensurePathForFile(arff_filename)
	arff.write(arff_filename)

	'''
	Write JSON
	'''
	json_filename = "../json/%s.json" %name
	ensurePathForFile(json_filename)
	writeJsonToFile(data, json_filename, True)

	
	return data

if __name__ == "__main__":
	print "Analyzing Final Fantasy XIV - Data"

	url = "http://www.ffxivguild.com/racial-stats-and-god-stats-guide/"
	html = readUrl(url)

	data = parse(url,"ffxiv_races")


	



