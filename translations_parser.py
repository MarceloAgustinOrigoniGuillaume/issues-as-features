import re
from reg_utils import *

class Statement:
	def __init__(self, description):
		self.description = ""
		self.table_headers = []
		self.table_rows = []

		for elem in re.findall(r"(.+)"+end_strip, description):
			self.append(elem)

	def add_table(self,*head):
		self.table_headers = head
		#print("---------------SETTING HEADERS!",head)

	def add_row(self, *vls):
		if(len(vls) != len(self.table_headers)):
			print("error different vls count! given ", len(vls)," headers have", len(self.table_headers))
			return
		#print("-------------------------ADDING ROW ",vls)

		self.table_rows.append(vls)


	def append(self, data):

		if (not data.endswith("|") or not data.startswith("|")):
			#print("--------------- NON TABLE?!", data)
			self.description+= data
			return


		rows = list (elem.strip() for elem in data[1:-1].split("|"))

		if(len(self.table_headers) == 0):
			self.add_table(*rows)
		else:
			self.add_row(*rows)

	def parse_rows(self):
		res = ""

		for row in self.table_rows:
			res+= "row: "+", ".join(row)+" ... "

		return res

	def parse_table(self):

		return "" if len(self.table_headers)== 0 else ": cols: "+", ".join(self.table_headers)+" ... "+self.parse_rows()


	def __repr__(self):
		return self.description+self.parse_table()

	def parse_table_desc(self):
		res = self.description

		if(len(self.table_headers) >0):
			res+= "\n|"+"|".join(self.table_headers)+"|"
			res+= "\n|"+"-|"*len(self.table_headers)
			for row in self.table_rows:
				res+= "\n|"+"|".join(row)+"|"

		return res



def replace_general(pattern, src, replacer):

	res = ""
	last_end = 0
	span= None
	grp = ""
	for match in re.finditer(pattern, src):
		span = match.span()

		res+= src[last_end:span[0]]
		last_end = span[1]

		res+= replacer(match)
			

	res+= src[last_end:]
	return res



translations = {}
trans_keys = []
pattern_all = r""

pattern_replace = r"(\s|\((?:\?\))?|\))"

PARSE_SEP = r"[\s\n]*->[\s\n]*"
TRANSLATION_PATT = r"'(.*)'"+PARSE_SEP+r"'(.*)'"


matcher_trans = re.compile(TRANSLATION_PATT)
matcher_replace = re.compile(pattern_replace)


def translation_replacer(match):
	item = match.group()
	if match != None:
		groups = match.groups()

		indGrp = 0
		while(indGrp < len(trans_keys) and groups[indGrp] == None):
			indGrp+=1

		if (indGrp == len(trans_keys)):
			print("--------------SOME ERROR NOT MATCHED ANYTHING?! at item ",item)
			return item

		#print("---------------- translation is ",indGrp, "WICH MEANS IS ",trans_keys[indGrp])
		match = re.match(trans_keys[indGrp], item)
		if(match == None):
			print("------- error failed to match and find groups on reg? itm ",item,"MATCHED ", groups[indGrp])
			return item

		groups = match.groups()
		#print("-----",groups)

		trans = translations[trans_keys[indGrp]]
		ind = 1

		for grp in groups:
			if(grp == None):
				break
			trans = trans.replace("?"+str(ind), str(grp))
			ind+=1

		return trans
	
	return end.append(item)


def translate(items):
	if(len(trans_keys) == 0):
		return list(str(item) for item in items)

	end = []
	for item in items:
		end.append(replace_general(pattern_all, str(item), translation_replacer))

	return end

#	return reg.replace(" ",r"\s").replace("(?)", " .* ").replace("(",r"\(")

def replace_base(src, grp_replace):

	res = ""
	last_end = 0
	span= None
	grp = ""
	for match in re.finditer(pattern_replace, src):
		span = match.span()
		grp = match.group()
		#print("match?!", grp, span)

		res+= src[last_end:span[0]]
		last_end = span[1]

		if grp == " ":
			res+=r"\s"
		elif grp== "(":
			res+=r"\("
		elif grp== ")":
			res+=r"\)"
		elif grp== "(?)":
			res+=grp_replace
			

	res+= src[last_end:]
	return res




#replace_base("untexto dos (cosa rara) y (?) fin!", "(.*)")

## original patt has (?) for any content param. So replace it for (.*)
def replace_grp(reg):
	return replace_base(reg, "(.*)")

def replace_ngrp(reg):
	return replace_base(reg, "(?:.*)")



def add_trans(original, replacement):
	global pattern_all

	key = replace_grp(original)

	if not key in translations:
		
		trans_keys.append(key)


		## ignore subgroups!!
		pattern_all = r"("+replace_ngrp(original)+r")" if len(trans_keys) == 1 else pattern_all+"|"+r"("+replace_ngrp(original)+r")"


	translations[key] = replacement
	
	#print("\n\nAFTER ADD TRANS!", trans_keys, pattern_all)

def log_add_trans(original, replacement):
	print("adding translation from '"+original+"'  TO  '"+replacement+"'")
	add_trans(original, replacement)

def parse_translations(file):
	print("------- parsing of",file,"started")
	hnd = open(file, "r")



	for obj in matcher_trans.findall(hnd.read()):
		log_add_trans(*obj)

	hnd.close()

	print("------- parsing of",file,"ended ")
