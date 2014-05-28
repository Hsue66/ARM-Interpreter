import sys
import collections


# read input.txt
lines = sys.stdin.readlines()

# read first line as start_point 
start_point = int(lines[0],16)


memory = dict()		# make original input as dict
res = dict()		# make new output as dict
flag =dict()		# make flag to differenciate string and integer

# read values and address to memory
for l in lines[1:]:
	try:
		[addr,value] = l.split(':')
		memory[addr] = int(value,16)		
	except:
		pass


# sort memory dict
omemory=collections.OrderedDict(sorted(memory.items()))

# change value to binary and strip '0b'
for n in omemory:
	omemory[n]=bin(omemory[n]).lstrip('0b')

# write new key(register) and value(result) to res
for k in omemory.keys():

	I=omemory[k][6]	
	branch = omemory[k][4:7]
	linkbit = omemory[k][7]	
	
	opcode = omemory[k][7:11]
	rd = int(omemory[k][16:20],2)
	rn = int(omemory[k][12:16],2)
	shift=omemory[k][25:27]
	if branch == '101':
		if linkbit == '0':
			# branch offset +
			if omemory[k][8] == '0':
				imm24 = int(omemory[k][8:],2)
				imm24 = hex(imm24*4 + 8 + int(k,16)).lstrip('0x')
				print imm24
				k = imm24
			# branch offset - 2's complement
			else:
				imm24 = int(omemory[k][8:],2)
				imm24 = int(bin((~imm24+1)&0xFF).lstrip('0b'),2)
				imm24 = hex(-imm24*4 + 8 + int(k,16)).lstrip('0x')
				print imm24
				k = imm24


