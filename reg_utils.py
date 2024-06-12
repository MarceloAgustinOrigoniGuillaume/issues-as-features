#any_content = r"(?:.*"+end_strip+r")*"
def opt(*options):
	return "|".join(options)

def grpn(reg, multiplicity = ""):
	return r"(?:"+reg+r")"+multiplicity

def grp(reg, multiplicity = ""):
	return r"("+reg+r")"+multiplicity

def any_except(key):
	return grpn(r"(?!"+key+r")(?:.|\s|\n|\t)", "*")


def simple_part_patter(mark):
	return r"("+mark+r")\s(.+)"+end_strip

def table_part_patter(mark):
	return r"("+mark+r")\s"+grp(any_content)


any_content = r".*"
end_strip = r"\n*\t*\s*"
