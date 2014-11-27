from contextlib import contextmanager
'''
Dumb Brainfuck code builder

Translates function calls into a buffer of Brainfuck code.
This class contains a lot of useful functions that abstract the brainfuck code
into familiar concepts such as variables and arithmetic.

All functions in the class are "non-destructive", they will not erase a variable used
by the function. This allows for more general-purpose programs. Do, however, consider
writing destructive functions as they might speed up the program significantly.

Usage:
    Create a BFConstuctor object
    Create your program
    To define custom functions, add them to the class and use them in the instance
        (See example program)
    The program is saved in the buffer variable, which you can print or save

'''
class BFConstructor:

    def __init__(self):
        self.buffer = []
        self.vars = [None]
        self.pointer = 0
        self.tempgen = self.tempgenerator()
    
    '''
    As of right now, this program uses strings to keep track of brainfuck variables (cells)
    This generator provides a simple way to dynamically create variables, as hardcoded
    variables may collide with each other.
    '''
    def tempgenerator(self):
        n = 0
        temp = 'temp'
        while True:
            yield temp + str(n)
            n += 1

    '''
    These functions are the meat of the program, at the very lowest level of abstraction.
    They correspond 1-to-1 with the brainfuck characters.
    '''
    def _right(self, steps):
        self.buffer.extend(['>' for _ in range(steps)])

    def _left(self, steps):
        self.buffer.extend(['<' for _ in range(steps)])

    def _inc(self, n):
        self.buffer.extend(['+' for _ in range(n)])

    def _dec(self, n):
        self.buffer.extend(['-' for _ in range(n)])

    def _print(self):
        self.buffer.append('.')

    def _input(self):
        self.buffer.append(',')

    def _begin(self):
        self.buffer.append('[')

    def _end(self):
        self.buffer.append(']')

    def _zero(self):
        self.buffer.extend(['[', '-', ']'])

    '''
    3 Different kinds of loops.
    The usage of context managers provide more intuitive loops and a syntax where
    indentation matters.
    '''
    @contextmanager
    def loop(self):
        self._begin()
        yield
        self._end()

    @contextmanager
    def for_(self, var):
        self.goto(var)
        with self.loop():
            yield
            self.goto(var)
            self._dec(1)

    @contextmanager
    def while_(self, var):
        self.goto(var)
        with self.loop():
            yield
            self.goto(var)

    '''
    Another core function. This will move the pointer to a variable var.
    '''
    def goto(self, var):
        index = self.vars.index(var)
        diff = index - self.pointer
        self.pointer += diff
        if diff > 0:
            self._right(diff)
        else:
            self._left(diff * -1)

    '''
    Tells the program that the variable var is now free to overwrite.
    '''
    def erase(self, var):
        for v in var:
            self.vars[self.vars.index(v)] = None

    '''
    Assign assigns a value value to a variable name, creates a variable name if necessary.
    To follow convention, name should be a string, and value can be either an integer or 
    a string (int to assign a number, string to assign the value of another variable)
    '''
    def assign(self, name, value):
        if name not in self.vars:
            if None in self.vars:
                self.vars[self.vars.index(None)] = name
            else:
                self.vars.append(name)
        self.goto(name)
        self._zero()
        if value not in self.vars:
            self._inc(value)
        else:
            tmp = self.tempgen.next()   
            self.assign(tmp, 0)
            self.goto(value)
            with self.loop():
                self._dec(1)
                self.goto(tmp)
                self._inc(1)
                self.goto(value)
            self.goto(tmp)
            with self.loop():
                self._dec(1)
                self.goto(value)
                self._inc(1)
                self.goto(name)
                self._inc(1)
                self.goto(tmp)
            self.erase([tmp])

    '''
    Reads input into a variable
    '''
    def input_(self, var):
        self.goto(var)
        self._input()

    '''
    Adds y to x. Afterwards, x will be x + y, and y will be y.
    '''
    def add_(self, x, y):
        tmp = self.tempgen.next()
        self.assign(tmp, y)
        self.goto(tmp)
        with self.loop():
            self._dec(1)
            self.goto(x)
            self._inc(1)
            self.goto(tmp)
        self.goto(x)
        self.erase([tmp])

    '''
    Subtract y from x
    '''
    def sub_(self, x, y):
        tmp = self.tempgen.next()
        self.assign(tmp, y)
        self.goto(tmp)
        with self.loop():
            self._dec(1)
            self.goto(x)
            self._dec(1)
            self.goto(tmp)
        self.goto(x)
        self.erase([tmp])

    '''
    Multiplies x by y
    '''
    def mul_(self, x, y):
        fac = self.tempgen.next()
        fac1 = self.tempgen.next()
        self.assign(fac, x)
        self.assign(fac1, y)
        self.assign(x, 0)
        self.goto(fac1)
        with self.loop():
            self._dec(1)
            self.add_(x, fac)
            self.goto(fac1)
        self.goto(x)
        self.erase([fac, fac1])

    '''
    Integer division of x by y will not work for y==0.
    '''
    def div_(self, x, y):
        ta = self.tempgen.next()
        na = self.tempgen.next()
        self.assign(ta, x)
        self.assign(na, y)
        self.assign(x, 0)
        self.goto(ta)
        with self.loop():
            self.goto(na)
            with self.loop():
                self._dec(1)
                self.goto(ta)
                self._dec(1)
                with self.notif_(ta):
                    with self.if_(na):
                        self.assign(na, 0)
                        self.goto(x)
                        self._dec(1)
                self.goto(na)
            self.goto(x)
            self._inc(1)
            self.assign(na, y)
            self.goto(ta)
        self.goto(x)
        self.erase([ta, na])
        
    '''
    Defines an if statement
    yields True if var is not 0
    '''
    @contextmanager
    def if_(self, var):
        tmp = self.tempgen.next()
        self.assign(tmp, var)
        self.goto(tmp)
        with self.loop():
            yield
            self.assign(tmp, 0)
        self.goto(var)
        self.erase([tmp])

    '''
    Comparison, less than.
    True if x is less than y
    '''
    @contextmanager
    def lt_(self, x, y):
        tmp = self.tempgen.next()
        tmp2 = self.tempgen.next()
        self.assign(tmp, x)
        self.assign(tmp2, y)
        self.goto(tmp2)
        with self.loop():
            self._dec(1)
            with self.notif_(tmp):
                self.assign(tmp2, 0)
                yield
            self._dec(1)
            self.goto(tmp2)
        self.goto(x)
        self.erase([tmp, tmp2])

    '''
    Greater than
    True if x is greater than y
    '''
    @contextmanager
    def gt_(self, x, y):
        tmp = self.tempgen.next()
        tmp2 = self.tempgen.next()
        self.assign(tmp, x)
        self.assign(tmp2, y)
        self.goto(tmp)
        with self.loop():
            self._dec(1)
            with self.notif_(tmp2):
                self.assign(tmp, 0)
                yield
            self._dec(1)
            self.goto(tmp)
        self.goto(x)
        self.erase([tmp, tmp2])

    '''
    Equal to
    True if x is equal to y
    This operation requires byte wrapping
    '''
    @contextmanager
    def eq_(self, x, y):
        tmp = self.tempgen.next()
        self.assign(tmp, x)
        self.sub_(tmp, y)
        with self.notif_(tmp):
            yield
        self.goto(x)
        self.erase([tmp])

    '''
    Assigns x to y mod x. y must be greater than x
    '''
    def mod_(self, x, y):
        na = self.tempgen.next()
        ta = self.tempgen.next()
        self.assign(na, x)
        self.assign(ta, y)
        self.goto(ta)
        with self.loop():
            self.goto(na)
            with self.loop():
                self._dec(1)
                self.goto(ta)
                self._dec(1)
                self.goto(na)
            self.assign(na, y)
            with self.lt_(ta, na):
                self.assign(x, ta)
                self.assign(ta, 0)
            self.goto(ta)
        self.goto(x)
        self.erase([na, ta])

    '''
    Notif
    yields True if var is 0
    '''
    @contextmanager    
    def notif_(self, var):
        tmp = self.tempgen.next()
        self.assign(tmp, 1)
        with self.if_(var):
            self.assign(tmp, 0)
        self.goto(tmp)
        with self.loop():
            yield
            self.assign(tmp, 0)
        self.goto(var)
        self.erase([tmp])

    '''
    Prints var
    '''
    def print_(self, var):
        self.goto(var)
        self._print()

    '''
    Ugly function ahead!
    Prints the numeric value of var.
    '''
    def print_num(self, var):
        tmp = self.tempgen.next()
        hun = self.tempgen.next()
        ten = self.tempgen.next()
        one = self.tempgen.next()
        self.assign(tmp, var)
        for n in [hun, ten, one]:
            self.assign(n, 0)
        with self.for_(tmp):
            self.goto(one)
            self._inc(1)
            with self.gt_(one, 9):
                self.goto(one)
                self._zero()
                self.goto(ten)
                self._inc(1)
            with self.gt_(ten, 9):
                self.goto(ten)
                self._zero()
                self.goto(hun)
                self._inc(1)
        with self.if_(hun):
            self.add_(hun, 48)
            self.print_(hun)
        with self.if_(ten):
            self.add_(ten, 48)
            self.print_(ten)
        self.add_(one, 48)
        self.print_(one)
        self.erase([tmp, hun, ten, one])

if __name__ == '__main__':
    print "Don't call directly."
