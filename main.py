import os
import translations_parser as ghtrans
import gherking_to_table as ghfeat


def parse_path(url, mark, repl):
	return url.replace(mark, repl)
MARK_SCRIPT_URL = "-sc/"

if(__name__ == "__main__"):

	import sys
	base_url = sys.argv[0][:-len("main.py")]
	ghfeat.parse_path = lambda url: parse_path(url, MARK_SCRIPT_URL, base_url)
	
	print("Directory root for script?",base_url)
	if(len(sys.argv)>1):
		ghfeat.load_feat(ghfeat.parse_path(sys.argv[1]))


		if(len(sys.argv)>2):
			print("FOR NOW IGNORE trans at ",ghfeat.parse_path(sys.argv[2]))
			#ghtrans.parse_translations(ghfeat.parse_path(sys.argv[2]))


	command = input("action>")
	while(ghfeat.exec(command, ghfeat.feature)):
		command = input("action>")