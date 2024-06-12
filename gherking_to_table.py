import re,os
from translations_parser import *
from reg_utils import *

scenario_title_gherking = "Scenario:"
feature_title_gherking = "Feature:"
given_mark_gherking = "Given"
when_mark_gherking = "When"
then_mark_gherking = "Then"
and_mark_gherking = "And"

valid_mark_pat = grpn(opt(given_mark_gherking, when_mark_gherking, then_mark_gherking, and_mark_gherking))

title_pat = r".*"+feature_title_gherking+r"\s(.+)\n"


given_pat = table_part_patter(given_mark_gherking)

and_pat = table_part_patter(and_mark_gherking)

when_pat = simple_part_patter(when_mark_gherking)
then_pat = simple_part_patter(then_mark_gherking)

scenario_title = scenario_title_gherking+r"\s(.+)"+end_strip

scenario_data =  grp(any_except(scenario_title_gherking))# anything but... scenario keyword

token_data =  grp(valid_mark_pat)+r"\s"+grp(any_except(valid_mark_pat+r"\s"))# anything but... scenario keyword




print("---------------- pat:\n",scenario_title+scenario_data)
print("\n\n")

class Scenario:
	def __init__(self, parts):

		#match_found = re.match(scenario_title,text)

		#if(match_found == None):
		#	raise Exception("invalid format!! NO scenario found on feature!")


		self.title = parts[0]

		print("\n----loading scenario::",self.title)

		#parts =parts[1:]

		self.given = []
		self.when = []
		self.then = []

		self.parse_parts(re.findall(token_data, parts[1]))

	def name(self):
		return self.title

	def pre_conditions(self):
		return self.given


	def actions(self):
		return self.when


	def post_conditions(self):
		return self.then


	def build_table(self, table, groups, ind):
		return

	def build_content(self,container, groups, ind):
		container.append(groups[ind])
		return ind+2

	def parse_parts(self, parts):
		last_list = []
		mark = ""
		for part in parts:
			mark = part[0]

			if(given_mark_gherking == mark):
				last_list = self.given
			elif(when_mark_gherking == mark):
				last_list = self.when
			elif(then_mark_gherking == mark):
				last_list = self.then

			last_list.append(Statement(part[1]))


class Feature:
	def __init__(self, text):
		match_found = re.match(title_pat, text)

		if(match_found == None):
			raise Exception("invalid format!! NO feature found!")

		self.title = match_found.group(1)
		print("\n----loading feature::",self.title)


		#print("RES",self.title)


		self.scenarios = []



		self.title = match_found.group(1)

		text = text[match_found.end():].strip()
		#print("FIND ALL?!")
		#match_found = re.match(scenario_title+scenario_data, text)

		#print("MATCH FOUND ",match_found.group()) 
		match_found = re.findall(scenario_title+scenario_data,text)#re.match(r"(?:"+scenario_title+r"(.+))+",text)




		print("FOUND", len(match_found),"Scenarios")


		for scene in match_found:
			#print("scene",scene)
			self.scenarios.append(Scenario(scene))




	def toText(self):
		res = "FEATURE: "+self.name()+" ";

		for scene in self.scenarios:
			res += str(scene.pre_conditions())+"\n"+str(scene.actions())+"\n"+str(scene.post_conditions())

		return res

	def name(self):
		return self.title

	def __repr__(self):
		return self.toText()


part_join = " y "




def parse(feat):
	output = "# "+feat.name()+"\n"


	for scene in feat.scenarios:
		output+= "## Escenario: "+scene.name()+"\n"
		output+= "### Dado: "+parse_items_text(scene.pre_conditions())+"\n"
		output+= "### Cuando: "+parse_items_text(scene.actions())+"\n"
		output+= "### Entonces: "+parse_items_text(scene.post_conditions())+"\n"

	return output



def parse_table(feat):
	output = "# "+feat.name()+"\n"

	output+= "\n|Escenario|Contexto|Evento|Resultado\n|-|-|-|-|"



	#print("\n--------------PATTERN ALL ",pattern_all,"\n\n", trans_keys)





	for scene in feat.scenarios:
		output+="\n|"+scene.name()+"|"+parse_items(scene.pre_conditions())+"|"+parse_items(scene.actions())+"|"+parse_items(scene.post_conditions())+"|"

	return output

def parse_items(items):
	return part_join.join(translate(items))


def parse_items_text(items):
	return ("\n###"+part_join).join(translate(list(item.parse_table_desc() for item in items)))




def load_feat(path):
	global feature
	hnd = open(path,"r") # file name!
	feature = Feature(hnd.read())

	hnd.close()

	#print("-----------loaded ",path, feature)

def check_match(feat, pattern, baseTrans):
	if len(translations) == 0:
		print("NO TRANS!")
		return

	matched = 0
	



	for scene in feat.scenarios:
		for part in scene.pre_conditions():
				print("MATCHED COUNT ",matched)


def parse_path(url):
	return url


def exec(comm, feat):
	global feature
	#print("FEAT IS ",feat)
	if(comm == "table"):
		print("'"+parse_table(feat)+"'")
		return True

	if(comm == "parse"):
		print("'"+parse(feat)+"'")
		return True		


	if(comm == "cls"):
		os.system("cls")
		return True

	if(comm == "parts"):
		#print("------- patt", pattern_all)
		for scene in feat.scenarios:
			print("\n========= Scenario :: ",scene.name())
			print("GIVEN:: "#, scene.pre_conditions(), "TO\n"
				, translate(scene.pre_conditions()))

			print("WHEN:: "#, scene.actions(), "TO\n"
				,translate(scene.actions()))

			print("THEN:: "#, scene.post_conditions(), "TO\n"
				,translate(scene.post_conditions()))
		return True


	if(comm == "trans"):

		for translation in trans_keys:
			print("From '"+translation+"' TO '"+translations[translation]+"'")



		return True


	if(comm.startswith("trans ")):
		patt = re.match(r"^\"(.+)\"\s\"(.+)\"$",comm[6:])
		#print("FOUND IS ",patt)
		if(patt != None):
			#print("grps ", patt.groups()) 

			pattern = patt.group(1)
			baseTrans = patt.group(2)

			print("-------------------------",pattern)


			print(check_match(feat, pattern, baseTrans))

	if(comm.startswith("ld ")):
		try:
			load_feat(parse_path(comm[3:]))
		except Exception as e:
			print("FAILED LOAD FEAT !!",e)
			feature = feat 

		return True

	if(comm.startswith("ltrans ")):
		try:
			parse_translations(parse_path(comm[7:]))
		except Exception as e:
			print("FAILED LOAD Translations! ",e)

	if(comm == ""):
		print("---------- ended")
		return False
	print("---------- not recognized command '"+comm+"'")

	return True

feature = None

if __name__ == "__main__":
	import sys


	load_feat(sys.argv[1])

	command = input("action>")

	while(exec(command, feature)):
		command = input("action>")