import requests
import re 
from textwrap import wrap
from collections import Counter
import string 


code = "https://s3.eu-central-1.amazonaws.com/csh-static/arnies_secret/218977e6210d1ea602af94f1bbc296e5ae0a86cfa7c15a4149cafb938d3d29dd.txt"
decoder = {"ZERO" : "0", "ONE": "1"}

def get_code():
	return requests.get(code).text

def parse_code(code):
	triplets = [re.split("(ZERO|ONE)", x) for x in re.split("\s+", code)]
	triplets = [x for x in triplets if len(x) == 3]
	pairs = [(digit, count) for junk, digit, count in triplets]
	return [decoder[digit] * len(count) for digit, count in pairs]

def parse_code2(code):
	triplets = [re.split("(ZERO|ONE)", x) for x in re.split("\s+", code)]
	triplets = [x for x in triplets if len(x) == 3]
	pairs = [(digit, count) for junk, digit, count in triplets]
	d = {1:"", 2:"", 3:""}
	for digit, count in pairs:
		# print len(count), decoder[digit] 
		d[len(count)] = d[len(count)]+decoder[digit] 
	return d



def decode_code(code):
	num = code.replace("ZERO", "0").replace("ONE", "1")
	# print re.search(num, "!").group(0)
	return num.replace("!", "") * (len(re.search("!+", num).group(0)))


def codes_to_3d(codes):
	d3 = {1:"", 2:"", 3:""}
	for code in codes:
		for i in range(len(code)):
			d3[i+1] += code[i]
	return d3

def codes_to_two(codes):
	d3 = {1:"", 2:""}
	for code in codes:
		for i in range(len(code)):
			if i == 0:
				d3[1] += code[i]
			else:
				d3[2] += code[i]
	return d3

def interweave(arr1, arr2):
	if len(arr2) < len(arr1):
		return interweave(arr2, arr1)
	out = ""
	for i in range(len(arr1)):
		out += arr1[i]
		out += arr2[i]
	return out + arr2[len(out):]

raw = get_code()
codes = raw.split()
one_string = ""
decoded = [decode_code(code) for code in codes]

byte_array = wrap(one_string, 8)
byte_dic_alt = codes_to_two(decoded)

dic = codes_to_3d(decoded)
byte_array1 = wrap(dic[1], 8)
byte_array2 = wrap(dic[2], 8)
byte_array3 = wrap(dic[3], 8)
byte_array_alt = wrap(interweave(dic[3], dic[2]), 8)

print "dic2", len(dic[2])
print "dic3", len(dic[3])
print "dic1", len(dic[1])



print byte_array_alt

print len(byte_array1)
print "length alt array", len(byte_array_alt)

# print len(byte_array1)
# print len(byte_array2)
# print len(byte_array3)
message = "".join([chr(int(b,2)) for b in byte_array1])
message2 = "".join([chr(int(b,2)) for b in byte_array_alt])
# print message
print message2


splited = message.split()
lower = [x for x in splited if x.islower()]
upper = [x for x in splited if x.isupper()]

# for i, msg in enumerate(splited):
# 	if not i % 3:
# 		print msg


# print "".join([chr(int(b,2)) for b in byte_array2])
# print "".join([chr(int(b,2)) for b in byte_array3])



# codes2 = parse_code2(raw)
# for code in codes2.values():
# 	print int(code, 2)