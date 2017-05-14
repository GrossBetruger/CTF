import subprocess 
from sys import stdin
import re

def parse_rpn(expression):
    """ Evaluate a reverse polish notation """
 
    stack = []
 
    for val in re.split('\s+', expression):
        if val in ['-', '+', '*', '/']:
            op1 = stack.pop()
            op2 = stack.pop()
            if val=='-': result = op2 - op1
            if val=='+': result = op2 + op1
            if val=='*': result = op2 * op1
            if val=='/': result = op2 / op1
            stack.append(result)
        else:
            stack.append(int(val))
 
    return stack.pop()


def p_hacking(p, challenge):
    try:
        answer = str(parse_rpn(challenge))
    except ValueError:
        print "the flag is:", challenge
        return 
    print "answer:", answer
    res = p.stdin.write(str(answer) + "\n")
    p.stdin.flush()
    response = p.stdout.readline().strip()
    print "response", response
    return p_hacking(p, response)

if __name__ == "__main__":
    p = subprocess.Popen(["nc", "35.158.25.165", "10096"],
     stdin=subprocess.PIPE, stdout=subprocess.PIPE, bufsize=10000)
    for i in range(4):
        line =  p.stdout.readline().strip()
        print line
        print i 
        if i == 3:
            p_hacking(p, line)
            # answer = str(parse_rpn(line))
            # print "answer:", answer
            # res = p.stdin.write(str(answer) + "\n")
            # p.stdin.flush()
            # second_challenge = p.stdout.readline().strip()
            # print "second challenge", second_challenge
            # second_answer = str(parse_rpn(second_challenge))
            # print "second answer", second_answer
            # res = p.stdin.write(str(second_answer) + "\n")
            # p.stdin.flush()
            # third_challenge = p.stdout.readline().strip()
            # print "third_challenge", third_challenge
            # third_answer = str(parse_rpn(third_challenge))
            # print "third answer", third_answer
            # res = p.stdin.write(str(third_answer) + "\n")
            # p.stdin.flush()
            # print p.stdout.readline().strip()



    # print a.stdout.read()

