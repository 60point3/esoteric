from __future__ import print_function

class Brainfuck:
    
    def __init__(self):
        self.ptr = 0
        self.tape = [0]
        self.commands = '' 
        self.inbuffer = ''
        self.outbuffer = []
        self.index = 0#for debugging purposes
        self.inindex = 0

    def readcode(self, commands, code=False):
        if code:
            self.commands = commands
            return
        with open(commands)as f:
            for line in f:
                self.commands += line

    def readin(self, commands, code=False):
        if code:
            self.inbuffer = commands
            return
        with open(commands)as f:
            for line in f:
                self.inbuffer += line.strip()
        self.inbuffer += chr(10)

    def execute(self):
        index = 0
        while True:
            try:
                cmd = self.commands[index]
            except IndexError:
                break
            if cmd is '+':
                self.tape[self.ptr] += 1
                if self.tape[self.ptr] > 255:
                    self.tape[self.ptr] = 0
            elif cmd is '-':
                self.tape[self.ptr] -= 1
                if self.tape[self.ptr] < 0:
                    self.tape[self.ptr] = 255
            elif cmd is '>':
                self.ptr += 1
                if len(self.tape) == self.ptr:
                    self.tape.append(0)
            elif cmd is '<':
                self.ptr -= 1
                if self.ptr < 0:
                    raise PointerException('Attempted negative pointer')
            elif cmd is '.':
                #self.outbuffer.append(chr(self.tape[self.ptr]))
                print(chr(self.tape[self.ptr]), end='')
            elif cmd is ',':
                self.tape[self.ptr] = ord(self.inbuffer[self.inindex])#ord(raw_input()[0])
                self.inindex += 1
            elif cmd is '[':
                if self.tape[self.ptr] == 0:
                    match = 1 
                    while not (self.commands[index] is ']' and match == 0):
                        index += 1
                        if self.commands[index] is ']':
                            match -= 1
                        elif self.commands[index] is '[':
                            match += 1
            elif cmd is ']':
                if self.tape[self.ptr] is not 0:
                    match = 1
                    while not (self.commands[index] is '[' and match == 0):
                        index -= 1
                        if self.commands[index] is '[':
                            match -= 1
                        elif self.commands[index] is ']':
                            match += 1
            index += 1
            self.index = index

'''
Exception to be raised whenever the pointer reaches an illegal value
'''
class PointerException(Exception):
    pass

if __name__ == '__main__':
    bf = Brainfuck()
    bf.readcode('out.bf')
    bf.readin('hello.bf')
    try:
        bf.execute()
    except PointerException:
        print('PointerException')
        print('ptr\t', bf.ptr)
        print('tape\t', bf.tape)
        print(bf.commands[:bf.index+1])
    print(''.join(bf.outbuffer))
    print(bf.tape)
