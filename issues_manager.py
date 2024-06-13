import json,sys, os,re
import gherking_to_table as ghfeat

from reg_utils import *

base_url = sys.argv[0][:-len("issues_manager.py")]

file_temp = base_url+"tempfile.txt"
res_temp = base_url+"restemp.txt"



def write_desc_temp(desc):
	hnd = open(file_temp,"w")
	hnd.write(desc)
	hnd.close()

def read_desc_temp():
	hnd = open(file_temp,"r")
	res = hnd.read()
	hnd.close()
	return res

def write_res_temp(res):
	hnd = open(res_temp,"w")
	hnd.write(res)
	hnd.close()

def read_res_temp():
	hnd = open(res_temp,"r")
	res = hnd.read()
	hnd.close()
	return res



print("-------- url base for script", base_url)

patt_name_iss = r"(\d+)\s*\-\s*(.+)"

if(len(sys.argv)>1 and sys.argv[1]!= "list"): 
	act = sys.argv[1]
	
	#print("SHOULD DO ACTION?! '"+act+"'")

	if(act == "parse"):
		comm = "scn" if (len(sys.argv) == 2) else "scn "+ (" ".join(sys.argv[2:]))
		comm+= " -o \""+file_temp+"\""
		print("command is '"+comm+"'")

		out = os.popen(comm).read()
		#print(out)

		print("\n---------------------------------")
		result = json.loads(read_desc_temp())

		print("RES ", len(result))
		issues = json.loads(os.popen("gh issue list --json title,number").read())
		numbers = []
		for issue in issues:
			numbers.append(issue["number"])

		print("NUMBERS !",numbers)

		for elem in result:

			num= int(elem["number"])

			if(num in numbers):
				print(" path at ", elem["path"] , "name ", elem["title"], "num ", num, "updating description!")
				

				#print("----------------------------------- desc\n"+elem["body"]+"\n\n")
				write_res_temp(elem["body"])
				
				out = os.popen("gh issue edit "+str(num)+" --body-file \""+res_temp+"\"").read()
				print(out)#read_res_temp())
			else:
				print(" path at ", elem["path"] , "name ", elem["title"], "num ", num, "not found in issues!!!!")
	elif(act == "showf"):
		base = sys.argv[2]+"/" if len(sys.argv) > 2 else os.getcwd() 
		for feat in ghfeat.search_features_on(base):
			print("\n----------FOUND A FEATURE!\n", ghfeat.parse_feat_meta(feat))
	elif(act == "help"):
		print("command 'iss renamei' renames issues to match issue number on title")
		print("command 'iss createf <base_dir>' creates features for issues in repository on the base dir, default is current one")
		print("command 'iss showf <base_dir>' shows features found on base dir, default is current")
		print("command 'iss list' shows current repository issues")
		print("command 'iss parse <feat_querie> <translations file> -t' updates issues that match in number given the translations,"
			+"-t changes to use table description ... <feat_querie> may be a file, a directory, or -us<number> <base_dir> to select one user story!")
	elif(act == "createf"):
		jsonIssues = json.loads(os.popen("gh issue list --json title,number").read())

		name = ""
		base = ""
		if(len(sys.argv) > 2):
			base = sys.argv[2]+"/"

		for item in jsonIssues:
			name_file = str(item["number"]) if int(item["number"])>=10 else "0"+str(item["number"])
			res = re.match(patt_name_iss, item["title"])
			if(res == None):
				name_file = "us"+name_file+"_"+item["title"].replace(" ", "_")+".feature"
			else:
				name_file = "us"+name_file+"_"+res.group(2).replace(" ", "_")+".feature"

			# verify starts with number?
			print("--Found on git!",item, "should create file === '"+base+name_file+"'")

			hnd = open(base+name_file, "a+")

			hnd.close()

	elif(act == "renamei"):
		jsonIssues = json.loads(os.popen("gh issue list --json title,number").read())

		num = ""
		for item in jsonIssues:
			num = str(item["number"]) if int(item["number"])>=10 else "0"+str(item["number"])

			# verify starts with number?
			res = re.match(patt_name_iss, item["title"])
			if(res == None):
				item["title"] = num+" - "+item["title"]

			elif res.group(1) != num: ## group 1 is the number!
				item["title"] = num+" - "+res.group(2) # group 2 is the name itself!
			else: ## dont change/rename?!
				print(item, "is named correctly!")
				continue
			## rename?!

			#name = item["title"] if item["title"].startswith(name+" - ") else name+" - "+item["title"]

			#item["title"] = name
			print("-------Found on git to rename!",item)
			out = os.popen("gh issue edit "+str(item["number"])+" -t \""+item["title"]+"\"").read()
			print(out)
	exit()



print("LISTING ISSUES ON REPOSITORY!")


jsonIssues = json.loads(os.popen("gh issue list --json title,number").read())


for item in jsonIssues:
	print("--Found on git!",item)
