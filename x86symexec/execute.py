#!/usr/bin/env python

import symath
from registers import *
from instructions import *

def _get_src_value(op, context):
  if isinstance(op, symath.Number):
    return op

  a,b = symath.wilds('a b')
  vals = symath.WildResults()

  op = op.substitute(context)

  if op.match(DEREF(a, b), vals):
    if op in context:
      return context[op]

  return op

def _get_dst_value(op, context):
  return _get_src_value(op, context)

def execute_instruction(ist, context):
  a,b,c = symath.wilds('a b c')
  vals = symath.WildResults()

  def _set_big_reg(dst, src):
    if src in (AX, BX, CX, DX, SI, DI, BP, SP):
      src = symath.symbols('E' + src.name) & 0xffff
    elif src in (AL,BL,CL,DL):
      src = symath.symbols('E' + src.name[0] + 'X') & 0xff
    elif src in (AH,BH,CH,DH):
      src = (symath.symbols('E' + src.name[0] + 'X') & 0xff00) >> 8

    if dst in (AX,BX,CX,DX,SI,DI,BP,SP):
      edst = symath.symbols('E' + dst.name)
      context[edst] = (edst.substitute(context) & 0xffff0000) | src
    elif dst in (AL,BL,CL,DL):
      edst = symath.symbols('E' + dst.name[0] + 'X')
      context[edst] = (edst.substitute(context) & 0xffffff00) | src
    elif dst in (AH,BH,CH,DH):
      edst = symath.symbols('E' + dst.name[0] + 'X')
      context[edst] = (edst.substitute(context) & 0xffff00ff) | (src << 8)
    else:
      context[dst] = src

  if ist.match(Mov(a, b), vals):
    src = _get_src_value(vals.b, context)
    _set_big_reg(vals.a, src)

  elif ist.match(Push(a), vals):
    src = _get_src_value(vals.a, context)
    esp = _get_dst_value(ESP, context) - 4
    context[DEREF(0x4, esp)] = src
    context[ESP] = esp

  elif ist.match(Pop(a), vals):
    dst = _get_dst_value(vals.a, context)
    src = _get_src_value(DEREF(0x4, ESP), context)
    esp = _get_dst_value(ESP, context) + 4
    _set_big_reg(dst, src)
    context[ESP] = esp

  elif ist.match(Sub(a, b), vals):
    dst = _get_dst_value(vals.a, context)
    src = _get_src_value(vals.b, context)
    _set_big_reg(vals.a, dst - src)
    _set_big_reg(EFLAGS, dst - src)

  elif ist.match(Add(a, b), vals):
    dst = _get_dst_value(vals.a, context)
    src = _get_src_value(vals.b, context)
    _set_big_reg(vals.a, dst + src)
    _set_big_reg(EFLAGS, dst + src)

  elif ist.match(Xor(a, b), vals):
    dst = _get_dst_value(vals.a, context)
    src = _get_src_value(vals.b, context)
    _set_big_reg(vals.a, dst ^ src)
    _set_big_reg(EFLAGS, dst ^ src)

  elif ist.match(Or(a, b), vals):
    dst = _get_dst_value(vals.a, context)
    src = _get_src_value(vals.b, context)
    _set_big_reg(vals.a, dst | src)
    _set_big_reg(EFLAGS, dst | src)

  elif ist.match(And(a, b), vals):
    dst = _get_dst_value(vals.a, context)
    src = _get_src_value(vals.b, context)
    _set_big_reg(vals.a, dst & src)
    _set_big_reg(EFLAGS, dst & src)

  elif ist.match(Shl(a, b), vals) or ist.match(Sal(a, b), vals):
    dst = _get_dst_value(vals.a, context)
    src = _get_src_value(vals.b, context)
    _set_big_reg(vals.a, dst << src)
    _set_big_reg(EFLAGS, dst << src)

  elif ist.match(Shr(a, b), vals) or ist.match(Sar(a, b), vals):
    dst = _get_dst_value(vals.a, context)
    src = _get_src_value(vals.b, context)
    _set_big_reg(vals.a, dst >> src)
    _set_big_reg(EFLAGS, dst >> src)

  elif ist.match(Cmp(a, b), vals):
    dst = _get_dst_value(vals.a, context)
    src = _get_src_value(vals.b, context)
    _set_big_reg(EFLAGS, dst - src)

  elif ist.match(Test(a, b), vals):
    dst = _get_dst_value(vals.a, context)
    src = _get_src_value(vals.b, context)
    _set_big_reg(EFLAGS, dst & src)

  elif ist.match(Call(a,b,c), vals):
    if not isinstance(vals.b, symath.Number) or not isinstance(vals.c, symath.Number):
      raise BaseException("Call must have numbers for parameters 2 and 3")
    dst = _get_dst_value(vals.a, context)
    _set_big_reg(EAX, CALLRESULT(EAX, dst, vals.c))
    _set_big_reg(ECX, CALLRESULT(ECX, dst, vals.c))
    _set_big_reg(EDX, CALLRESULT(EDX, dst, vals.c))
    _set_big_reg(EFLAGS, CALLRESULT(EFLAGS, dst, vals.c))
    _set_big_reg(ESP, ESP.substitute(context) + vals.b)

  else:
    raise BaseException("instruction %s not understood" % (ist,))
