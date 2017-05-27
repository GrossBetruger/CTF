
import json 
from collections import Counter
import enchant

english_dict = enchant.Dict("en_US")

readme =\
"""
Each row starts with a key letter.

Algebric repr:
encryption - c = (p + k) % 26
decryption - p = (c - k) % 26

looks like this algo works with modulo 13
"""


def read_raw(fname):
	with open(fname) as f:
		return f.read()


def parse_raw(raw):
	return clear_white_space([[x.replace(" ", "") for x in row.split("|")[1:-1]]
	 for row in raw.split("\n")[1:-1:2]])

# def parse_raw_crypt(raw):
# 	return [[x.replace(" ", "") for x in row.split("|")[1:-1]]
# 	 for row in raw.split("\n")[1:-1:2]]

def clear_white_space(matrix):
	return [row for row in matrix if not all([x == "" for x in row ])]

def encrypt(message, key):
	def do_work(message=message, key=key):
		message = list(message.upper())
		key = key.upper()
		i = int()
		while message:
			i = i % len(key)
			k = key[i]
			next_letter = message.pop(0)
			c = map_get(k, next_letter)
			# print next_letter, k, "cypher", c
			yield c 
			i += 1
	return "".join(list(do_work()))


cmap = read_raw("map")

cgram = parse_raw(read_raw("cryptogram"))
cmap = parse_raw(read_raw("map"))

def map_get(k, p):
	return cmap[ord(k)-64][ord(p)-64]

def cgram_get(k, p):
	# print k, p
	row = cmap[ord(k)-64]
	return [chr(i + 64) for i, x in enumerate(row) if  x == p]


def inversify(cgram):
	inv = ""
	for x in range(1, len(cgram)):
		for y in cgram:
			inv += y[x]
	return inv 

def load_commons():
	with open("common") as f:
		return json.load(f)

flat = "".join(["".join(x) for x in cgram][1:-1])
inverse =  inversify(cgram)
commons = load_commons()


def guess(key):
	in_flats = int()
	in_inverse = int()
	for common in [val for val in commons.values() if len(val) > 3]:
		plain = common
		cypher =  encrypt(plain, key)
		assert len(cypher) == len(plain)
		if cypher in flat :
			in_flats += flat.count(cypher) 
	return in_flats

def count_eng(plain):
	score = int()
	for word in commons.values():
		score += plain.count(word)
	return score

def get_freq_letter(plain):
	counter = Counter()
	counter.update(plain)
	return list(reversed(sorted(dict(counter).items(), key=lambda a:a[1])))

def decrypt(message, key, out="", threshold=20):
	message = message.upper()
	key = key.upper()
	i = int()
	while message:
		i = i % len(key)
		k = key[i]
		p = message[0]
		try:
			first, second = cgram_get(k, p)
		except ValueError as e:
			# print p, k
			quit()
		message = message[1:]
		decrypt(message, key, out+first, threshold=threshold)
		# decrypt(message, key, out+second, threshold=threshold)
	c = count_eng(out)
	print c, out
	letters = "".join([x[0] for x in get_freq_letter(out)])
	# print get_freq_letter(out)
	# print letters
	if letters.startswith("ETA"):
		print out, letters
		print "key", key

def simp_guess(key, known):
	in_flats = int()
	in_inverse = int()
	cypher =  encrypt(known, key)
	assert len(cypher) == len(known)
	if cypher in flat :
		in_flats += flat.count(cypher) 
	return in_flats

def simp_decrypt(message, key, factor):
	if message == " ":
		return " "
	out = ""
	message = message.upper()
	key = key.upper()
	i = int()

	while message:
		i = i % len(key)
		k = key[i]
		p = message[0]
		assert len(cgram_get(k, p)) == 2
		out += cgram_get(k, p)[factor]
		message = message[1:]

	return out

chars = [chr(i) for i in range(65, 91)]




def create_chars(seed):
	normal = [chr(i) for i in range(65, 91)]
	new = ""
	for i in range(seed, seed + 26):
		new += normal[i % 26]
	return new


def try_rows():
	all_dec = []
	for i in range(0, 26):
		for factor in [0, 1]:
			for row in cgram[1:]:
				spaced = "".join([x if x != "" else " " for x in row[1:]])
				plain = [simp_decrypt(word, create_chars(i), factor) for word in spaced.split()]
				all_dec += [plain]
	return  all_dec

def try_columns():
	inverse = zip(*cgram[1:])

	all_dec = []
	for i in range(0, 26):
		for factor in [0, 1]:
			for row in inverse[1:]:
				row = list(row)
				for gap in [6, 13, 16, 22]:
					row.insert(gap, " ")
				# print row
				spaced = "".join([x if x != "" else " " for x in row])
				# print spaced
				# break

				plain = [simp_decrypt(word, create_chars(i), factor) for word in spaced.split()]
				all_dec += [plain]
	return all_dec


def get_cyptoGram():
	clean = []
	raw = read_raw("cryptogram")
	for row in raw.split("\n")[2:]:
		clean_row = [x.replace(" ", "") if x.replace(" ", "") else " " for x in row.split("|")]
		if set(row) != set("+-"):
			clean.append(clean_row[2:])

	return ["".join(c) for c in clean]

if __name__ == "__main__":
	keys = [create_chars(i) for i in range(15, 17)]
	key = chars
	crypted = get_cyptoGram()
	all_dec = []
	lookup = ["ME", "YOU", "US", "WARNED", "ABOUT"]
	threshold = 0
	for key in keys:
		for factor in [0, 1]:
			for row in crypted:
				# pointer = i  #% len(chars)
				all_row = []
				for l in row:
					print l
					plain = simp_decrypt(l, key, factor) #for word in row.split()]
					print plain, factor, i
					all_row += plain
				all_dec += ["".join(all_row)]
				# pointer += 1
			# for _ in all_dec:
			# 	print _
	all_dec = [x.split() for x in all_dec]
	good = [x for x in all_dec if len([y for y in x if y in lookup]) > threshold
			or 0] #len([y for y in x if english_dict.check(y) > threshold])

	for i in all_dec:
		for j in i:
			if j in lookup:
				print j

	for _ in good:
		print _
	quit()



	all_dec = try_rows()
	good = [x for x in all_dec if len([w for w in x if english_dict.check(w)]) > 2]
	for g in good:
		print g

	quit()

	for k, v in total.iteritems():
		print k, v
	counter = Counter()
	counter.update(best)
	print list(reversed(sorted(dict(counter).items(), key=lambda a: a[1])))
	quit()

	problem = 242
	wild_card = ""
	# for c in chars:
	decrypt(flat[:60], wild_card, threshold=30)
	print "done"
	quit()


	final = "flag"
	for _ in range(10):
		max_score = int()
		choice = ""
		for word in chars:
			g =  final + word
			scores = [simp_guess(g, "be"),simp_guess(g, "to"),simp_guess(g, "of"), simp_guess(g, "in")]
			score = sum(scores)
			if score > max_score and word not in final:
				max_score = score
				choice = word
		final += choice
		print "final", final
	quit()
	score = []
	for word in commons.values():
	# for char in [chr(i) for i in range(97, 123)]:
		key = word
		g = "into"
		# for char in [chr(i) for i in range(97, 123)] + [""]:
		# 	key+char
		last = guess(key)
		new = guess(g + key)
		if new > last:
			print new, last
			print "new guess", key+g
		score.append((last, key))
	score = list(reversed(sorted(score, key=lambda a: a[0])))
	threshold = 3
	print score[0:10]





		
	
