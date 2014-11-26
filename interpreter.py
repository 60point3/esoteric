from bf import BFConstructor as BFC
from contextlib import contextmanager

if __name__ == '__main__':

    '''
    Specific functions for memory-reading
    Constants used in functions
    '''
    
    program = 'p'
    mem = 'm'

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
                    with bfc.while_('a'):#Antag; ej '[]'
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
            
    print ''.join(bfc.buffer)
