import sys
import collections


# read input.txt
lines = sys.stdin.readlines()

# read first line as start_point 
start_point = int(lines[0],16)


memory = dict()		# make original input as dict
res = dict()		# make new output as dict
flag =dict()		# make flag to differenciate string and integer
imm24=0
# read values and address to memory
for l in lines[1:]:
	try:
		[addr,value] = l.split(':')
		addr = addr.lstrip()
		memory[addr] = int(value,16)		
	except:
		pass


# sort memory dict
omemory=collections.OrderedDict(sorted(memory.items()))

# change value to binary and strip '0b'
for n in omemory:
	omemory[n]=bin(omemory[n]).lstrip('0b').zfill(32)

# write new key(register) and value(result) to res
for m in omemory.keys():
	if m == omemory.keys()[0]:
		k=m
		
	else:
		k=hex(int(k,16)+4).lstrip('0x')
	
	branch = omemory[k][4:7]
	linkbit = omemory[k][7]	
	I=omemory[k][6]		
	opcode = omemory[k][7:11]
	rd = int(omemory[k][16:20],2)
	rn = int(omemory[k][12:16],2)
	shift=omemory[k][25:27]
	# branch
	if branch == '101':
		if linkbit == '0':
			# branch offset +
			if omemory[k][8] == '0':
				imm24 = int(omemory[k][8:],2)
				k = hex(imm24*4 + 8 + int(k,16)).lstrip('0x')
				#print imm24
			# branch offset - 2's complement
			else:
				imm24 = int(omemory[k][8:],2)
				imm24 = int(bin((~imm24+1)&0xFF).lstrip('0b'),2)
				k= hex(-imm24*4 + 8 + int(k,16)).lstrip('0x')
				#print imm24
		else:
			print 'bl'
		branch = omemory[k][4:7]
		linkbit = omemory[k][7]
		I=omemory[k][6]	
		opcode = omemory[k][7:11]
		rd = int(omemory[k][16:20],2)
		rn = int(omemory[k][12:16],2)
		shift=omemory[k][25:27]
	# mov
	if opcode=='1101':
		if I=='0':	# operand is register
			rm = int(omemory[k][28:32],2)
			res[rd]=res[rm]
			flag[rd] = '0'

		else:		# operand is integer
			operand = int(omemory[k][24:32],2)
			res[rd] = operand
	
			flag[rd] = '0'
		print res[rd]
	# add
	elif opcode=='0100':
		if I=='0':	# operand is register	
			rm = int(omemory[k][28:32],2)		
			res[rd]=res[rm]+res[rn]
			flag[rd] = '0'

		else:		# operand is integer
			operand = int(omemory[k][24:32],2)	
			res[rd] = operand+res[rn]
	
			flag[rd] = '0'

		print "res:",res[rd]

	# swi
	elif opcode=='1000':
		n=15
		res[n] = (int(k,16)+ 8)

		flag[n] = '0'
		break;


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

