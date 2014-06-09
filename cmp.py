import sys
import collections

def do_shift(rd,shift,k):
	amount=int(omemory[k][20:25],2)
		
	# lsl
	if shift=='00':
		result=res[rm]<<amount
					
		flag[rd] = '0'

	# lsr
	elif shift=='01':
		temb= bin(res[rm]).lstrip('0b')
		temb=temb.zfill(8)
		tema= temb[:len(temb)-amount]
		result=tema.zfill(8)
				
		flag[rd] = '1'
				
	# asr
	elif shift=='10':
		result=res[rm]>>amount
	
		flag[rd] = '0'
					
	# ror
	elif shift=='11':
		temt= bin(res[rm]).lstrip('0b')
		temt=temt.zfill(8)
		tema= temt[:len(temt)-amount]
		temb=temt[len(temt)-amount:]
		result=temb+tema

		flag[rd] = '1'
	return result

# read input.txt
lines = sys.stdin.readlines()

# read first line as start_point 
start_point = int(lines[0],16)


memory = dict()		# make original input as dict
res = dict()		# make new output as dict
flag =dict()		# make flag to differenciate string and integer
imm24=0
cmptemp = 0		#set cmptemp's base value

# read values and address to memory
for l in lines[1:]:
	try:
		[addr,value] = l.split(':')
		addr=  addr.lstrip()
		memory[addr] = int(value,16)		
	except:
		pass


# sort memory dict
omemory=collections.OrderedDict(sorted(memory.items()))

# change value to binary and strip '0b'
for n in omemory:
	omemory[n]=bin(omemory[n]).lstrip('0b').zfill(32)



# write new key(register) and value(result) to res
k = '0'
while(1):
	if k == '0':
		k = omemory.keys()[0]
	else:
		k=hex(int(k,16)+4).lstrip('0x')
	
	branch = omemory[k][4:7]
	linkbit = omemory[k][7]	

	S = omemory[k][11]

	cond=omemory[k][0:4]

	#codition check

	#always(normal processing instruction)
	if cond == '1110': pass
	#eq
	elif cond == '0000':
		if cmptemp == 0: pass
		else: continue
	#ne
	elif cond == '0001':
		if ~(cmptemp == 0): continue
		else: pass
	#ge
	elif cond == '1010':
		if cmptemp >= 0: pass
		else: continue
	#le
	elif cond == '1101':
		if cmptemp <= 0: pass
		else: continue
	#gt
	elif cond == '1100':
		if cmptemp > 0: pass
		else: continue
	#lt
	elif cond == '1011':
		if cmptemp < 0: pass
		else: continue
	
	else: pass

	
	#Bx lr
	if omemory[k][8:] == '001011111111111100011110':
		k = hex(int(res[14],16)+4).lstrip('0x')
	# branch
	if branch == '101':
		if linkbit == '0':
			# branch offset +
			if omemory[k][8] == '0':
				imm24 = int(omemory[k][8:],2)
				k = hex(imm24*4 + 8 + int(k,16)).lstrip('0x')

			# branch offset - 2's complement
			else:
				imm24 = int(omemory[k][8:],2)
				imm24 = int(bin((~imm24+1)&0xFF).lstrip('0b'),2)
				k= hex(-imm24*4 + 8 + int(k,16)).lstrip('0x')

		else:
			res[14] = k.zfill(8)
			flag[14] = '1'
			# branch offset +
			if omemory[k][8] == '0':
				imm24 = int(omemory[k][8:],2)
				k = hex(imm24*4 + 8 + int(k,16)).lstrip('0x')

			# branch offset - 2's complement
			else:
				imm24 = int(omemory[k][8:],2)
				imm24 = int(bin((~imm24+1)&0xFF).lstrip('0b'),2)
				k= hex(-imm24*4 + 8 + int(k,16)).lstrip('0x')

	I=omemory[k][6]		
	opcode = omemory[k][7:11]
	rd = int(omemory[k][16:20],2)
	rn = int(omemory[k][12:16],2)
	shift=omemory[k][25:27]

	#processing
	# cmp
	if opcode=='1010':
		cmptemp = 0
		if I=='0':	# operand is register
			rm = int(omemory[k][28:32],2)
			
			if omemory[k][20:28] !='00000000':
				cmptemp=res[rn]-do_shift(rd,shift,k)
			else:
				cmptemp = res[rn]-res[rm]

		else:		# operand is integer
			operand = int(omemory[k][24:32],2)
			cmptemp = res[rn]-operand
	
	# mov
	elif opcode=='1101':
		if I=='0':	# operand is register
			rm = int(omemory[k][28:32],2)
			
			if omemory[k][20:28] !='00000000':
				res[rd]=do_shift(rd,shift,k)
		
			else:
				res[rd]=res[rm]

				flag[rd] = '0'

		else:		# operand is integer
			operand = int(omemory[k][24:32],2)
			res[rd] = operand
	
			flag[rd] = '0'
	
	# mul
	elif (omemory[k][4:10]=='000000')and(omemory[k][24:28]=='1001'):
		rd=int(omemory[k][12:16],2)
		rm=int(omemory[k][28:32],2)
		rs=int(omemory[k][20:24],2)		
		res[rd]=res[rm]*res[rs]
		if S =='1':
			cmptempt = res[rd]
				
		flag[rd]='0'	

	# add
	elif opcode=='0100':
		if I=='0':	# operand is register
			rm = int(omemory[k][28:32],2)
			
			if omemory[k][20:28] !='00000000':
				res[rd]=do_shift(rd,shift,k)+res[rn]
				if S =='1':
					cmptemp = res[rd]
					flag[rd] = '0'
			else:
				res[rd]=res[rm]+res[rn]
                                if S =='1':
                                	cmptemp = res[rd]
				
				flag[rd] = '0'

		else:		# operand is integer
			operand = int(omemory[k][24:32],2)
			res[rd] = operand+res[rn]
                        if S =='1':
                                cmptemp = res[rd]
	
			flag[rd] = '0'


	# sub
	elif opcode=='0010':
		if I=='0':	# operand is register
			rm = int(omemory[k][28:32],2)
			
			if omemory[k][20:28] !='00000000':
				res[rd]=res[rn]-do_shift(rd,shift,k)
				if S == '1':
					cmptemp = res[rd]
					
					flag[rd] = '0'
			else:
				res[rd]=res[rn]-res[rm]
				if S == '1':
					cmptemp = res[rd]
				
				flag[rd] = '0'

		else:		# operand is integer
			operand = int(omemory[k][24:32],2)
			res[rd] = res[rn]-operand
			if S == '1':
				cmptemp = res[rd]
			
			flag[rd] = '0'

	# rsb
	elif opcode=='0011':
		if I=='0':	# operand is register
			rm = int(omemory[k][28:32],2)
			
			if omemory[k][20:28] !='00000000':
				res[rd]=do_shift(rd,shift,k)-res[rn]
				if S =='1':
					cmptemp = res[rd]

					flag[rd] = '0'
			else:
				res[rd]=res[rm]-res[rn]
				if S =='1':
					cmptemp = res[rd]
				flag[rd] = '0'

		else:		# operand is integer
			operand = int(omemory[k][24:32],2)
			res[rd] = operand-res[rn]
                        if S =='1':
                                cmptemp = res[rd]

			flag[rd] = '0'
	

	# and
	elif opcode == '0000' and branch != '101':
	
		if I=='0':	#operand is register
			rm = int(omemory[k][28:32],2)
			result=bin(res[rn]&res[rm]).lstrip('0b')
			res[rd]=result.zfill(8)
			
			flag[rd]='1'
		else:
			operand=int(omemory[k][24:32],2)
			result=bin(res[rn]&operand).lstrip('0b')
			res[rd]=result.zfill(8)
			flag[rd]='1'

	# orr
	elif opcode == '1100':
	
		if I=='0':	#operand is register
			rm = int(omemory[k][28:32],2)
			result=bin(res[rn]|res[rm]).lstrip('0b')
			res[rd]=result.zfill(8)
			
			flag[rd]='1'
		else:
			operand=int(omemory[k][24:32],2)
			result=bin(res[rn]|operand).lstrip('0b')
			res[rd]=result.zfill(8)
			flag[rd]='1'
				
	# eor
	elif opcode == '0001':
	
		if I=='0':	#operand is register
			rm = int(omemory[k][28:32],2)
			result=bin(res[rn]^res[rm]).lstrip('0b')
			res[rd]=result.zfill(8)
			
			flag[rd]='1'
		else:
			operand=int(omemory[k][24:32],2)
			result=bin(res[rn]^operand).lstrip('0b')
			res[rd]=result.zfill(8)
			flag[rd]='1'

	# mvn
	elif opcode == '1111':
	
		if I=='0':	#operand is register
			rm = int(omemory[k][28:32],2)
			res[rd]=bin(~res[rm]&0xFF).lstrip('0b')
			
			flag[rd]='1'
			
		else:
			operand=int(omemory[k][24:32],2)
			res[rd]=bin(~operand&0xFF).lstrip('0b')
			
			flag[rd]='1'
			
	
	# bic
	elif opcode == '1110':
	
		if I=='0':	#operand is register
			rm = int(omemory[k][28:32],2)
			result=bin(~res[rm]&0xFF&res[rn]).lstrip('0b')
			res[rd]=result.zfill(8)

			flag[rd]='1'
		else:
			operand = int(omemory[k][24:32],2)
			result=bin(~operand&0xFF&res[rn]).lstrip('0b')
			res[rd]=result.zfill(8)
			
			flag[rd]='1'		


	# swi
	elif opcode=='1000':
		n=15
		res[n] = (int(k,16)+ 8)

		flag[n] = '0'
		break
	else:
		n=15
		res[n]= (int(k,16)+ 8)
		flag[n] = '0'
		break

reg = res.items()	# make res as list
reg.sort()		# sort res list



# initialize unexist register
for k in range(16):

	if k !=reg[k][0]:
		flag[k]='0'
		reg.insert(k,(k,0))


# output format
showlist = ['r0:','r1:','r2:','r3:','r4:','r5:','r6:','r7:','r8:',
	'r9:','r10:','r11:','r12:','r13 sp:','r14 lr:','r15 pc:']

# display registers and values
for i in range(len(showlist)):
	if flag[i][0]=='0':	
		print '%-8s' % showlist[i],'%0.8x' % reg[i][1]
	else:
		print '%-8s' % showlist[i], reg[i][1]	


