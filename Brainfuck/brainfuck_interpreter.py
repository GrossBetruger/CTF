import time
from sys import argv


LEFT_BRACKET = "["
RIGHT_BRACKET = "]"
HELLO_WORLD = "++++++++++[>+++++++>++++++++++>+++>+<<<<-]>++.>+.+++++++..+++.>++.<<+++++++++++++++.>.+++.------.--------.>+.>."
MEMORY_SIZE = 22


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def overflow(num):
    return num % 256


def paint(printable, color):
    num_str = str(printable)
    return color + num_str + bcolors.ENDC


def load_code(filename):
    return open(filename).read()


class Interpreter():
    def __init__(self, code, input_array, debuggable=False, sleep=0):
        self.code = code
        self.code_length = len(code)
        self.input_array = input_array
        self.debuggable = debuggable
        self.sleep = sleep


    memory_map = [0] * MEMORY_SIZE
    data_pointer = 0
    input_array_pointer = 0
    code_pointer = 0

    def get_data(self):
        return self.memory_map[self.data_pointer]

    def pointer_increment(self):
        self.data_pointer += 1

    def pointer_decrement(self):
        self.data_pointer -= 1

    def data_increment(self):
        self.memory_map[self.data_pointer] = overflow(self.memory_map[self.data_pointer] + 1)

    def data_decrement(self):
        self.memory_map[self.data_pointer] = overflow(self.memory_map[self.data_pointer] - 1)

    def output_data_pointer(self):
        output_byte = self.memory_map[self.data_pointer]
        print paint(output_byte, bcolors.OKGREEN), paint(chr(output_byte), bcolors.OKGREEN)

    def left_bracket(self):
        if self.get_data() == 0:
            while self.code[self.code_pointer] != RIGHT_BRACKET:
                self.code_pointer += 1

    def right_bracket(self):
        if self.get_data() != 0:
            while self.code[self.code_pointer] != LEFT_BRACKET:
                self.code_pointer -= 1

    def read_input(self):
        next_input = self.input_array[self.input_array_pointer]
        self.memory_map[self.data_pointer] = next_input
        self.input_array_pointer += 1
        if self.debuggable:
            print paint(next_input, bcolors.BOLD)

    def print_memory_map(self):
        print " ".join([paint(num, bcolors.OKBLUE) if i == self.data_pointer else str(num) for i, num in enumerate(self.memory_map)])

    instruction_map = {">" : pointer_increment,
                       "<" : pointer_decrement,
                       "+" : data_increment,
                       "-" : data_decrement,
                       "." : output_data_pointer,
                       "," : read_input,
                       LEFT_BRACKET : left_bracket,
                       RIGHT_BRACKET : right_bracket}

    def read_code(self):
        while(self.code_pointer < self.code_length):
            next_opcode = self.code[self.code_pointer]
            if self.debuggable:
                print paint(next_opcode, bcolors.FAIL)
            self.instruction_map.get(next_opcode)(self)
            self.code_pointer += 1
            if self.debuggable:
                print
                self.print_memory_map()
                # time.sleep(self.sleep)


if __name__ == "__main__":
    start_array = [100, 116, 90, 115, 135, 104, 107, 115, 95, 86, 83, 117, 109, 99, 49, 118, 51, 121, 86, 111]
    offsets = [int(len(x.strip())-1) if "-" in x else int(len(x.strip())-1)*-1 for x  in open('offsets').readlines()]
    start_plus_offset = [x + y for x, y in zip(start_array, offsets)]
    print start_plus_offset
    print "".join(chr(x) for x in start_plus_offset)
    print offsets
    code = load_code(argv[1])
    sleep = float(argv[2])
    interpreter = Interpreter(code,
                              start_plus_offset, debuggable=True, sleep=sleep)
    interpreter.read_code()
