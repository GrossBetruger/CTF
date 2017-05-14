import requests
import re 
from textwrap import wrap

code = "https://s3.eu-central-1.amazonaws.com/csh-static/arnies_secret/218977e6210d1ea602af94f1bbc296e5ae0a86cfa7c15a4149cafb938d3d29dd.txt"
decoder = {"ZERO" : "0", "ONE": "1"}

def get_code():
	return requests.get(code).text

def parse_code(code):
	triplets = [re.split("(ZERO|ONE)", x) for x in re.split("\s+", code)]
	triplets = [x for x in triplets if len(x) == 3]
	pairs = [(digit, count) for junk, digit, count in triplets]
	return [decoder.get(digit) * len(count) for digit, count in pairs]


one_string = ""
codes = parse_code(get_code())
total = int()
for c in codes:
	one_string += c

total = int()
for c in wrap(one_string, 12):
	total += int(c, 2) 
print  total
# chunks = wrap(one_string, 8)
# for l in chunks:
# 	if chr((int(l, 2)+48)%256).isdigit():
# 		print chr((int(l, 2)+48)%256) 
