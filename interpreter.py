from bf import BFConstructor as BFC
from contextlib import contextmanager

'''
Example program for the Brainfuck Code-constructor.

This program will, when run, output brainfuck-code for a functional brainfuck
interpreter
'''

if __name__ == '__main__':

    '''
    Meow
    '''
    
    program = 'p'

    '''
    Reads from stdin and puts it in the program memory, when it encounters
    ASCII 10 it will stop reading.
    '''
    def readProgram(self):
        self._right(1)
        self._input()
        with self.loop():
            self._right(2)
            self._input()
            self._dec(10)
            with self.loop():
                self._inc(10) #Exit on newline
                self._left(1)
            self._right(1)
        self._right(1)
        self._inc(1)
        self._left(4)
        with self.loop():
            self._left(2)
        self._right(1)

    '''
    Copies the character at the current program pointer into working memory
    '''
    def get(self, var):
        self.goto(program)
        self._right(2)
        with self.loop():
            self._right(2)
        self._left(1)
        with self.loop():
            self._dec(1)
            self._right(1)
            self._inc(1)
            with self.loop():
                self._left(2)
            self.goto(var)
            self._inc(1)
            self.goto(program)
            self._right(2)
            with self.loop():
                self._right(2)
            self._left(3)
        self._right(1)
        with self.loop():
            self._dec(1)
            self._left(1)
            self._inc(1)
            self._right(1)
        self._inc(1)
        with self.loop():
            self._left(2)

    '''
    Increments of every non-zero program pointer. This is used when entering
    a loop to ease returning to the starting point
    '''
    def loopinc(self):
        self.goto(program)
        self._right(2)
        with self.loop():
            self._inc(1)
            self._right(2)
        self._left(2)
        self._dec(1)
        with self.loop():
            self._left(2)

    '''
    Decrements all non-zero program pointers. This is used to return to the starting
    point of a loop.
    '''
    def loopdec(self):
        self.goto(program)
        self._right(2)
        with self.loop():
            self._dec(1)
            self._right(2)
        self._left(1)
        with self.loop():
            self._left(2)
        self._right(1)
    
    '''
    This moves to the memory as a context manager.
    '''
    @contextmanager
    def mem(self):
        self.goto(program)
        self._right(1)
        with self.loop():
            self._right(2)
        self._right(4)
        with self.loop():
            self._right(2)
        self._left(1)
        yield
        self._left(1)
        with self.loop():
            self._left(2)
        self._left(4)
        with self.loop():
            self._left(2)
        self._right(1)

    '''
    Add the custom functions to the base class and create a instance of it

    Below is mostly code defined in BFConstructor.
    '''
    BFC.readProgram = readProgram
    BFC.get = get
    BFC.mem = mem
    BFC.loopinc = loopinc
    BFC.loopdec = loopdec
    bfc = BFC()
    bfc.assign('<', ord('<'))
    bfc.assign('>', ord('>'))
    bfc.assign('+', ord('+'))
    bfc.assign('-', ord('-'))
    bfc.assign('.', ord('.'))
    bfc.assign(',', ord(','))
    bfc.assign('[', ord('['))
    bfc.assign(']', ord(']'))
    bfc.vars.extend([None for _ in range(8)])
    bfc.vars.append(program)
    bfc.goto(program)
    bfc.readProgram()
    bfc.assign('a', 0)
    bfc.get('a')
    with bfc.while_('a'):
        with bfc.eq_('a', '+'):
            with bfc.mem():
                bfc._inc(1)
        with bfc.eq_('a', '-'):
            with bfc.mem():
                bfc._dec(1)
        with bfc.eq_('a', '>'):
            with bfc.mem():
                bfc._right(1)
                bfc._inc(1)
                bfc._left(1)
        with bfc.eq_('a', '<'):
            with bfc.mem():
                bfc._left(1)
                bfc._dec(1)
                bfc._left(1)
        with bfc.eq_('a', '.'):
            with bfc.mem():
                bfc._print()
        with bfc.eq_('a', '['):
            '''
            The below code is mostly pure brainfuck code,
            which definitely falls under the dirty-hack category
            '''
            bfc.loopinc()
            with bfc.mem():
                bfc._right(1)
                bfc._inc(1)
                bfc._left(1)
                with bfc.loop():
                    bfc._right(1)
                    bfc._dec(1)
                    bfc._left(1)
                    with bfc.loop():
                        bfc._dec(1)
                        bfc._left(1)
                        bfc._inc(1)
                        bfc._right(1)
                bfc._right(1)
                with bfc.loop():
                    with bfc.loop():
                        bfc._left(2)
                    bfc._left(4)
                    with bfc.loop():
                        bfc._left(2)
                    bfc._right(1)
                    bfc.get('a')
                    with bfc.while_('a'):
                        bfc.assign('a', 0)
                        bfc.get('a')
                        with bfc.eq_('a', ']'):
                            bfc.assign('a', 0)
                    bfc.goto(program)
                    bfc._right(1)
                    with bfc.loop():
                        bfc._right(2)
                    bfc._right(4)
                    with bfc.loop():
                        bfc._right(2)
                    bfc._left(2)
                    bfc._dec(1)
                bfc._left(2)
                with bfc.loop():
                    bfc._dec(1)
                    bfc._right(1)
                    bfc._inc(1)
                    bfc._left(1)
                bfc._inc(1)
                bfc._right(1)
                bfc._dec(1)
        with bfc.eq_('a', ']'):
            bfc.loopdec()
        bfc.assign('a', 0)
        bfc.get('a')
    
    #Print the buffer
    print ''.join(bfc.buffer)
