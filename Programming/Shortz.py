"""
Shortz
One slightly famous conjecture in math which hasn't been proved yet is called Collatz: 
https://en.wikipedia.org/wiki/Collatz_conjecture
We found a locked device for which the one-time password is generated using a variation of this algorithm. 
To break it, we want to ask for your help in generating one of the one-time password.
The device uses a variation of the Collatz conjecture on INTEGER numbers. 
We'll call it Shortz.
What we know: 
1. We know the device ALWAYS divides by 4 on even numbers, 
even ones not divisible by 4, so the next step after 6 would be 6/4 == 1. 
2. We know the device always reached a stop condition even with the alternative behaviour, not sure if there was another change in the code...
The device uses two functions when generating passwords: 
1. Shortz(n) -> the number of steps from n until we reach a stop condition 
2. ShortzSum(n) -> the sum of all the steps in Shortz(n) including n itself
Here is an example: 
Calculating Shortz(5) would have the following values: 
5 
16 
4 
1 
Thus ShortzSum(5) is 26, while Shortz(5) is 3 (5->16->4->1)
Help us break the device's password!
Calculate this number: 
ShortzSum(645399044249100) * Shortz(98325112)
Send us the resulting one-time token."""

def shortz(n, depth=0):
	while n >= 2:
		# print depth, n
		if n % 2 == 0:
			n = n/4
			depth += 1 
		else:
			n = 3*n +1
			depth += 1
	return depth

def shortz_sum(n):
	summary = n
	while n >= 2:
		if n % 2 == 0:
			n = n/4
			summary += n 
		else:
			n = 3*n +1
			summary += n
	return summary 


if __name__ == "__main__":
	import sys
	sys.setrecursionlimit(18000)
	print shortz(5)
	print shortz_sum(5)
	print shortz(98325112) * shortz_sum(645399044249100)