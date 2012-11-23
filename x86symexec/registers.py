#!/usr/bin/env
from symath import symbols,wilds,WildResults,symbolic

CALLRESULT = symbols('CALLRESULT')
DEREF = symbols('DEREF')
EAX,EBX,ECX,EDX = symbols('EAX EBX ECX EDX')
EDI,ESI,ESP,EBP = symbols('EDI ESI ESP EBP')
EFLAGS = symbols('EFLAGS')

AX,BX,CX,DX,DI,SI,BP,SP = symbols('AX BX CX DX DI SI BP SP')
AL,AH,BL,BH,CL,CH,DL,DH = symbols('AL AH BL BH CL CH DL DH')

def reg_size(reg):
  a,b = wilds('a b')
  val = WildResults()

  if reg in (AX,BX,CX,DX,DI,SI,BP,SP):
    return symbolic(2)
  elif reg in (AL,AH,BL,BH,CL,CH,DL,DH):
    return symbolic(1)
  elif reg in (EAX,EBX,ECX,EDX,EDI,ESI,EBP,ESP,EFLAGS):
    return symbolic(4)
  elif reg.match(DEREF(a, b), val):
    return val.a
  else:
    raise BaseException('Unknown Register %s' % reg)

def is_register(exp):
  return exp in (AX,BX,CX,DX,DI,SI,BP,SP,AL,AH,BL,BH,CL,CH,DL,DH,EAX,EBX,ECX,EDX,EDI,ESI,EBP,ESP,EFLAGS)

def reg_mask(exp):
  if exp in (AL,BL,CL,DL):
    return 0xff & symbols('E%sX' % (exp.name[0]))
  elif exp in (AH,BH,CH,DH):
    return (0xff00 & symbols('E%sX' % (exp.name[0]))) >> 8
  elif exp in (AX,BX,CX,DX,DI,SI,BP,SP):
    return 0xffff & symbols('E%s' % (exp.name))
  else:
    return exp
