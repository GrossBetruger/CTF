import sys 
import re 

for line in re.split("(GET|HTTP).+", sys.stdin.read()):
	print line
	