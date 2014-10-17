from contextlib import contextmanager
'''
Brainfuck code builder
'''
class BFConstructor:

    def __init__(self):
        self.buffer = []
        self.vars = [None]
        self.pointer = 0
        self.tempgen = self.tempgenerator()
    
    def tempgenerator(self):
        n = 0
        temp = 'temp'
        while True:
            yield temp + str(n)
            n += 1

    def _right(self, steps):
        self.buffer.extend(['>' for _ in range(steps)])

    def _left(self, steps):
        self.buffer.extend(['<' for _ in range(steps)])

    def _inc(self, n):
        self.buffer.extend(['+' for _ in range(n)])

    def _dec(self, n):
        self.buffer.extend(['-' for _ in range(n)])

    def _zero(self):
        self.buffer.extend(['[', '-', ']'])

    def _print(self):
        self.buffer.append('.')

    def _input(self):
        self.buffer.append(',')

    def _begin(self):
        self.buffer.append('[')

    def _end(self):
        self.buffer.append(']')

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

    def goto(self, var):
        index = self.vars.index(var)
        diff = index - self.pointer
        self.pointer += diff
        if diff > 0:
            self._right(diff)
        else:
            self._left(diff * -1)

    def erase(self, var):
        for v in var:
            self.vars[self.vars.index(v)] = None

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

    #Reads input into variable
    def input_(self, var):
        self.goto(var)
        self._input()

    #Add y to x
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

    #Subtract y from x
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

    #Multiplies x by y
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

    #Integer division of x by y will not work for y==0.
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

    #True if x is less than y
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

    @contextmanager
    def eq_(self, x, y):
        tmp = self.tempgen.next()
        self.assign(tmp, x)
        self.sub_(tmp, y)
        with self.notif_(tmp):
            yield
        self.goto(x)
        self.erase([tmp])

    #Assigns x to y mod x. y must be greater than x
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

    def print_(self, var):
        self.goto(var)
        self._print()

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
    bfc = BFConstructor()
    bfc.assign('<', ord('<'))
    bfc.assign('>', ord('>'))
    bfc.assign('+', ord('+'))
    bfc.assign('-', ord('-'))
    bfc.assign('.', ord('.'))
    bfc.assign(',', ord(','))
    bfc.assign('[', ord('['))
    bfc.assign(']', ord(']'))
    bfc.assign('end', ord('e'))
    bfc.assign('in', 0)
    bfc.vars.extend([None for _ in range(11)])
    bfc.vars.append('array')
    bfc.assign('true', 1)
    with bfc.while_('true'):
        bfc.input_('in')
        with bfc.eq_('in', '>'):
            bfc.goto('array')
            bfc._right(2)
            with bfc.loop():
                bfc._right(2)
            bfc._inc(1)  
            with bfc.loop():
                bfc._left(2)
        with bfc.eq_('in', '<'):
            bfc.goto('array')
            bfc._right(2)
            with bfc.loop():
                bfc._right(2)
            bfc._left(2)
            bfc._dec(1)
            bfc._left(2)
            with bfc.loop():
                bfc._left(2)
        with bfc.eq_('in', '+'):
            bfc.goto('array')
            bfc._right(2)
            with bfc.loop():
                bfc._right(2)
            bfc._left(1)
            bfc._inc(1)
            bfc._left(1)
            with bfc.loop():
                bfc._left(2)
        with bfc.eq_('in', '-'):
            bfc.goto('array')
            bfc._right(2)
            with bfc.loop():
                bfc._right(2)
            bfc._left(1)
            bfc._dec(1)
            bfc._left(1)
            with bfc.loop():
                bfc._left(2)
        with bfc.eq_('in', '.'):
            bfc.goto('array')
            bfc._right(2)
            with bfc.loop():
                bfc._right(2)
            bfc._left(1)
            bfc._print()
            bfc._left(1)
            with bfc.loop():
                bfc._left(2)
        with bfc.eq_('in', 'end'):
            bfc.assign('true', 0)





    #bfc.assign('a', 1)
    #bfc.assign('b', 0)
    #bfc.assign('c', 0)
    #bfc.input_('c')
    #bfc.sub_('c', 48)
    #bfc.assign('d', 10)
    #with bfc.for_('c'):
        #bfc.print_num('a')
        #bfc.print_('d')
        #bfc.assign('tmp', 'a')
        #bfc.add_('a', 'b')
        #bfc.assign('b', 'tmp')
    print ''.join(bfc.buffer) 
