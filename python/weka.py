import datetime

class Arff(object):

	def __init__(self):
		self.title = "Untitled"
		self.sources = []
		self.relation = "default"
		self.attributes = []
		self.instances = 0

	def setTitle(self, title):
		self.title = title

	def addSource(self, source):
		self.sources.append(source)

	def setRelation(self, relation):
		self.relation = relation

	def addAttribute(self, attribute):
		self.attributes.append(attribute)
		if self.instances == 0:
			self.instances = len(attribute.values)
		elif self.instances != len(attribute.values):
			print "Warning! Mismatch in number of instances for attribute %s" %(attribute.name)

	def write(self, filename):
		f = open(filename, "w")

		## TITLE ##
		###########
		f.write('%% 1. Title: %s\n' %(self.title))

		## SPACING ##
		#############
		f.write('%\n')

		## SOURCES ##
		###########
		f.write('% 2. Sources:\n')
		for index,source in enumerate(self.sources):
			f.write('%%\t(%s) %s\n' %(chr(ord('a')+index), source))
		f.write('%%\t(%s) Date: %s\n' %(chr(ord('a')+len(self.sources)), str(datetime.datetime.today())))

		## SPACING ##
		#############
		f.write('%\n')

		## RELATION ##
		#############
		f.write('@RELATION %s\n' %self.relation)

		## EMPTY-SPACING ##
		f.write('\n')

		## ATTRIBUTE DECLARATION ##
		###########################
		for index,attribute in enumerate(self.attributes):
			if attribute.type == Attribute.TYPE_CLASS:
				f.write('@ATTRIBUTE %s %s\n' %(attribute.name, str(attribute.types).replace('[','{').replace(']','}').replace("'","")))
			else:
				f.write('@ATTRIBUTE %s %s\n' %(attribute.name, attribute.type))

		## EMPTY-SPACING ##
		f.write('\n')

		## DATA ##
		##########
		f.write('@DATA\n')

		## EMPTY-SPACING ##
		# f.write('\n')

		for instance in range(self.instances):
			for index, attribute in enumerate(self.attributes):
				#print "instance=%s, index=%s, attribute=%s" %(instance, index,attribute.name)
				if attribute.type == Attribute.TYPE_STRING:
					f.write('"%s"' %(attribute.values[instance]))
				else:
					f.write("%s" %(attribute.values[instance]))
				if index < len(self.attributes)-1:
					f.write(",")
				else:
					f.write("\n")

		f.close()

class Attribute(object):

	TYPE_NUMERIC = "NUMERIC"
	TYPE_CLASS = "CLASS"
	TYPE_STRING = "STRING"

	def __init__(self, name, type_, values = []):
		self.name = name
		self.type = type_
		self.values = values


class ClassAttribute(Attribute):

	def __init__(self, name, types_, values =[]):
		self.name = name
		self.type = Attribute.TYPE_CLASS
		self.values = values
		self.types = list(set(types_))
