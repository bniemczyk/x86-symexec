import x86symexec.instructions as inst
import unittest

from x86symexec.registers import *
from x86symexec.instructions import *
from x86symexec.execute import *

class TestExecution(unittest.TestCase):

  def setUp(self):
    pass

  def test_prolouge(self):
    ctx = {}
    execute_instruction(Push(EBP), ctx)
    execute_instruction(Mov(EBP, ESP), ctx)

    self.assertEqual(ctx[ESP], ESP - 4)
    self.assertEqual(ctx[EBP], ESP - 4)
    self.assertEqual(ctx[DEREF(0x4, ESP - 4)], EBP)

  def test_push_pop(self):
    ctx = {}
    execute_instruction(Push(EAX), ctx)
    execute_instruction(Push(EAX), ctx)
    execute_instruction(Pop(EBX), ctx)

    self.assertEqual(ctx[EBX], EAX)
    self.assertEqual(ctx[ESP], ESP - 4)
    self.assertEqual(ctx[DEREF(0x4, ESP - 8)], EAX)

  def test_arithmetic(self):
    ctx = {}

    execute_instruction(Xor(EAX, EAX), ctx)
    self.assertEqual(ctx[EAX], 0)

    execute_instruction(Mov(EAX, EBX), ctx)
    execute_instruction(Sub(EAX, EDX), ctx)
    self.assertEqual(ctx[EFLAGS], ctx[EAX])
    self.assertEqual(ctx[EAX], EBX - EDX)

  def test_bitextend(self):
    ctx = {}
    execute_instruction(Mov(AL, 0x4), ctx)
    self.assertEqual(ctx[EAX], (EAX & 0xffffff00) | 0x4)
    
    execute_instruction(Mov(BH, 0x4), ctx)
    self.assertEqual(ctx[EBX], (EBX & 0xffff00ff) | (0x4 << 8))

  def test_smallmov(self):
    ctx = {}
    execute_instruction(Mov(AL, BL), ctx)
    self.assertEqual(ctx[EAX], (EAX & 0xffffff00) | (EBX & 0xff))
    execute_instruction(Mov(CH, DH), ctx)
    self.assertEqual(ctx[ECX], (ECX & 0xffff00ff) | (EDX & (0xff << 8)))

  def test_call(self):
    ctx = {}
    execute_instruction(Mov(EAX, 0xdeadbeef), ctx)
    execute_instruction(Call(EAX, -4, 0xb0000000), ctx)
    self.assertEqual(ctx[EAX], CALLRESULT(EAX, 0xdeadbeef, 0xb0000000))
    self.assertEqual(ctx[EDX], CALLRESULT(EDX, 0xdeadbeef, 0xb0000000))
    self.assertEqual(ctx[ECX], CALLRESULT(ECX, 0xdeadbeef, 0xb0000000))
    self.assertEqual(ctx[EFLAGS], CALLRESULT(EFLAGS, 0xdeadbeef, 0xb0000000))
    self.assertEqual(ctx[ESP], ESP-4)

  def test_movzx(self):
    ctx = {}
    execute_instruction(Movzx(EAX, AH), ctx)
    self.assertEqual(ctx[EAX], (EAX & 0xff00) >> 8)
