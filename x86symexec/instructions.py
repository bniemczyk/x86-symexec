#!/usr/bin/env python

from symath import symbols

# data move
Mov = symbols('mov')
Movzx = symbols('movzx')
Movsx = symbols('movsx')
Push = symbols('push')
Pop = symbols('pop')
Lea = symbols('lea')

# arithmetic operations
Sub = symbols('sub')
Add = symbols('add')
Xor = symbols('xor')
And = symbols('and')
Or = symbols('or')
Shr = symbols('shr')
Shl = symbols('shl')
Sar = symbols('sar')
Sal = symbols('sal')

# comparison
Cmp = symbols('cmp')
Test = symbols('test')

# call instructions are weird in their definition
# they need to pass as a second argument the stack change
# and as the third argument the address at which the call
# takes place
# example: Call(0xdeadbeef, +4, 0xbeefbeef)
Call = symbols('call')
