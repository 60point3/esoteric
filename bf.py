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

    def _begin(self):
        self.buffer.append('[')

    def _end(self):
        self.buffer.append(']')

    @contextmanager
    def loop(self):
        self._begin()
        yield
        self._end()

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

    @contextmanager
    def if_(self, var):
        tmp = self.tempgen.next()
        self.assign(tmp, var)
        self.goto(tmp)
        with self.loop():
            yield
            self.assign(tmp, 0)
        self.erase([tmp])

    @contextmanager
    def lt_(self, var1, var2):
        pass

    def print_(self, var):
        self.goto(var)
        self._print()

if __name__ == '__main__':
    bfc = BFConstructor()
    bfc.assign('x', 50)
    bfc.assign('y', 50)
    bfc.add_('x', 'y')
    bfc.add_('y', 'y')
    bfc.print_('x')
    bfc.print_('y')
    print ''.join(bfc.buffer) 
