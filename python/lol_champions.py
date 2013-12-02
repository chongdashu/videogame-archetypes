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

def parse(url, name):
	#
	stats = urllib2.urlopen(url).read()

	soup = BeautifulSoup(stats)

	headings = [th.text.strip() for th in soup.find("table").find_all('th')]
	rows = [tr.find_all('td') for tr in soup.find("table").find_all('tr')[1:]]

	champions = []
	championsMap = {}

	for row in rows:
		champion = {}

		for i in range(0, len(headings)):
			heading = ''
			value = ''

			if i == 0:
				heading = 'Name'
				value = row[i].a['title']
			else:
				heading = headings[i]
				value = row[i].text.strip().replace('+','').replace('%', '')
				value = "0" if len(value)<1 else value

			champion[heading] = value
			
		champions.append(champion)
		championsMap[champion['Name']] = champion

	'''
	Create ARFF file.
	'''
	arff = weka.Arff()
	arff.setTitle("League of Legends | Champions | Level-18 Stats")
	arff.addSource("Creator: Chong-U Lim (culim@mit.edu)")
	arff.addSource("Research Group: Imagination, Computation, and Expression Lab (http://icelab.mit.edu)")
	arff.addSource("Institution: Massachusetts Institute of Technology (http://mit.edu)")
	arff.addSource("League of Legends - Wikia (http://leagueoflegends.wikia.com/)")
	arff.setRelation(name)

	for heading in headings[1:]:
		data = [champion[heading] for champion in champions]
		attr = weka.Attribute(heading, weka.Attribute.TYPE_NUMERIC, data)
		arff.addAttribute(attr)

	names = [champion['Name'] for champion in champions]
	attr = weka.Attribute('Name', weka.Attribute.TYPE_STRING, names)
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
	writeJsonToFile(championsMap, json_filename, True)


if __name__ == "__main__":
	print "Analyzing League of Legends - Champions Data"

	parse("http://leagueoflegends.wikia.com/wiki/Champion_statistics_at_level_18", "lol_champions_lvl18")
	parse("http://leagueoflegends.wikia.com/wiki/Base_champion_statistics", "lol_champions_base")

	url = "https://coderanger.net/champions.json"
	read = urllib2.urlopen(url).read()
	jd = json.JSONDecoder()
	stats = jd.decode(read.decode('utf-8'))


	



