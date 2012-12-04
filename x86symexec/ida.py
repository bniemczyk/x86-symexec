import distorm3
import idautils
import symath
import idc
from x86symexec.registers import *
from x86symexec.instructions import *
from x86symexec.execute import execute_instruction

def op_size(op):
  if op.dtyp in [0]:
    return 1
  elif op.dtyp in [1]:
    return 2
  elif op.dtyp in [2,3]:
    return 4
  elif op.dtyp in [4,7]:
    return 8

  raise "Unknown operand type"

def decode(ea=None):
  if ea == None:
    ea = idc.ScreenEA()
  ist = idautils.DecodeInstruction(ea)
  if ist == None:
    return None

  _bytes = map(lambda x: chr(idc.Byte(ea+x)), range(ist.size))
  _bytes = ''.join(_bytes)

  ist = distorm3.Decompose(ea, _bytes)[0]

  # distorm doesn't decode the operand logical size ie.. byte ptr, so use IDA for that
  for i in range(len(ist.operands)):
    idaop = idautils.DecodeInstruction(ist.address)[i]
    setattr(ist.operands[i], 'op_size', op_size(idaop))

  def _get_operand_sym(op):
    if op.type == 'Immediate':
      return symath.symbolic(op.value)
    elif op.type == 'AbsoluteMemoryAddress':
      return DEREF(op.op_size, op.disp)
    elif op.type == 'Register':
      return symath.symbols(distorm3.Registers[op.index].upper())
    elif op.type == 'AbsoluteMemory':
      rv = 0

      if op.index != None:
        rv += symath.symbols(distorm3.Registers[op.index].upper()) * op.scale
      if op.base != None:
        rv += symath.symbols(distorm3.Registers[op.base].upper())
      if op.disp != None:
        rv += symath.symbolic(op.disp)

      return DEREF(op.op_size, rv)
    else:
      raise BaseException("Unknown operand type %s (%s)" % (op.type, op))

  args = list(map(_get_operand_sym, ist.operands))

  if ist.mnemonic.lower() == 'call':
    spdiff = idc.GetSpDiff(ist.address+ist.size)
    return Call(args[0], spdiff, ist.address)
  else:
    return symath.symbolic(ist.mnemonic.lower())(*args)

def execEA(ctx, ea=None):
  if ea == None:
    ea = idc.ScreenEA()

  execute_instruction(decode(ea), ctx)
