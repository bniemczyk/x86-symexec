#!/usr/bin/env
from symath import symbols

CALLRESULT = symbols('CALLRESULT')
DEREF = symbols('DEREF')
EAX,EBX,ECX,EDX = symbols('EAX EBX ECX EDX')
EDI,ESI,ESP,EBP = symbols('EDI ESI ESP EBP')
EFLAGS = symbols('EFLAGS')

AX,BX,CX,DX,DI,SI,BP,SP = symbols('AX BX CX DX DI SI BP SP')
AL,AH,BL,BH,CL,CH,DL,DH = symbols('AL AH BL BH CL CH DL DH')
