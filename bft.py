from bfr import Brainfuck, PointerException
import unittest

class TestInterpreter(unittest.TestCase):

    def setUp(self):
        self.bf = Brainfuck()
        
    '''
    Run a Hello World Program and verify its output.
    '''
    def test_hello(self):
        print '[Interpreter] Testing Hello World!'
        helloworld = '''++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---
        .+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++.'''
        self.bf.read(helloworld, code=True)
        self.bf.execute()
        output = ''.join(self.bf.outbuffer)
        self.assertEqual(output, 'Hello World!\n')

    '''
    Verify an exception is raised when using a negative cell pointer
    '''
    def test_negative(self):
        print '\n[Interpreter] Testing negative pointer'
        negative = '<'
        self.bf.read(negative, code=True)
        self.assertRaises(PointerException, self.bf.execute)

    def test_wrapping_increment(self):
        print '\n[Interpreter] Testing incrementing wrapping'
        wrap_increment = '++++++++++++++++[>++++++++++++++++<-]>.'
        self.bf.read(wrap_increment, code=True)
        self.bf.execute()
        output = ''.join(self.bf.outbuffer)
        self.assertEqual(output, chr(0))

    def test_wrapping_decrement(self):
        print '\n[Interpreter] Testing decrementing wrapping'
        wrap_decrement = '-.'
        self.bf.read(wrap_decrement, code=True)
        self.bf.execute()
        output = ''.join(self.bf.outbuffer)
        self.assertEqual(output, chr(255))

if __name__ == '__main__':
    unittest.main()
