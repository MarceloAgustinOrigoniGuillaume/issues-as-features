import os,glob,re
import translations_parser as ghtrans
import gherking_to_table as ghfeat
from reg_utils import *
import json


def write_desc_file(file,desc):
	hnd = open(file,"w")
	hnd.write(desc)
	hnd.close()



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

	OUT_RES = None
	leftargs = sys.argv[2:]


	if(os.path.isfile(url)):
		feats.append(url)
	elif(os.path.isdir(url)):
		print("---------------loading .feature on directory ",url)

		feats = ghfeat.search_features_on(url)
		print("--------- Found ", len(feats) ," features")
	elif url.startswith("-us"):
		num= int(url[3:])
		if len(leftargs) == 0:
			print("when given a us number you should denote a directory for search! as second parameter")
			exit()
		url = leftargs[0]

		if not os.path.isdir(url):
			print("url is not a valid directory!")
			exit()

		for feat in ghfeat.search_features_on(url):
			if(int(ghfeat.parse_feat_meta(feat)["number"]) == num):
				feats.append(feat)
				print("---------- found ",feat)

		if len(feats) == 0:
			print("---------- did not find the us number!")
			exit()

		leftargs = leftargs[1:]

	else:
		print("---------- no valid feature path given!")
		exit()
	getter = ghfeat.parse
	outputFunc = lambda data: print(data)


	if(len(leftargs)>0):
		translations = ""
		tabled = False

		outflag = False 

		for arg in leftargs:
			if(arg == "-t"):
				tabled = True
			elif (arg == "-o"):
				outflag = True
			elif outflag:
				out = str(arg)
				outputFunc = lambda data: write_desc_file(out, data)
				outflag = False
			elif translations== "":
				translations = arg


		#print("TRANS '"+ghfeat.parse_path(translations)+"' from ", translations)
		if(translations != ""):
			ghtrans.parse_translations(ghfeat.parse_path(translations))

		if(tabled):
			getter = ghfeat.parse_table

	divider = grpn(opt(r"\\","/"))
	patt_part=grpn(exclude(divider),"?")+grpn(divider+any_except(divider), "*")

	patt_name = patt_part+divider+"us"+grp(exclude(grpn(r"\.feature")))+r"\.feature$"
	patt_issue = r"(\d+)_(.+)"



	#print("patt ", patt_name)



	wrote = False

	print("===========Starting parsing!")
	added = 0
	
	OUT_RES = []#"["
	
	for feat in feats:
		print("----------------- for feature :: ",feat, "----------- ")



		ghfeat.load_feat(feat)


		data = ghfeat.parse_feat_meta(feat)
		if(data != None):
			print("\n------------- description parsing for issue data: ",data, "count added before ",added)
			
			data["body"] = getter(ghfeat.feature)
			OUT_RES.append(data)
			
			added+=1

		matc = re.match(patt_name, feat)
		if(matc != None):
			parts = re.match(patt_issue, matc.groups()[0])
			if(parts == None):
				print("\n--------------invalid issue name in format?!")
				continue

	#OUT_RES+= "\n]"
	outputFunc(json.dumps(OUT_RES))

	#outputFunc(OUT_RES)
