import os
import translations_parser as ghtrans
import gherking_to_table as ghfeat


def parse_path(url, mark, repl):
	return url.replace(mark, repl)
MARK_SCRIPT_URL = "-sc/"

if(__name__ == "__main__"):

	import sys
	base_url = sys.argv[0][:-len("get_desc.py")]
	ghfeat.parse_path = lambda url: parse_path(url, MARK_SCRIPT_URL, base_url)
	
	print("Directory root for script?",base_url)
	if(len(sys.argv)==1):
		print("no url was passed to description getter!")
		exit()


	feats = []
	url = sys.argv[1]
	if(os.path.isfile(url)):
		feats.append(url)
	elif(os.path.isdir(url)):
		print("SHOULD SEARCH IN DIRECTORY FOR .feature?")





	getter = ghfeat.parse
	if(len(sys.argv)>2):
		translations = ""
		tabled = False

		for arg in sys.argv[2:]:
			if(arg == "-t"):
				tabled = True
			elif translations== "":
				translations = arg


		print("TRANS '"+ghfeat.parse_path(translations)+"' from ", translations)
		if(translations != ""):
			ghtrans.parse_translations(ghfeat.parse_path(translations))

		if(tabled):
			getter = ghfeat.parse_table

	for feat in feats:
		print("----------------- for feature :: ",feat)
		ghfeat.load_feat(feat)


		print("\n------------- description parsing")
		print(getter(ghfeat.feature))
