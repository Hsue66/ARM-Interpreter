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

#set cmptemp's base value
cmptemp = 0

# write new key(register) and value(result) to res
for k in omemory.keys():

	I=omemory[k][6]		
	opcode = omemory[k][7:11]
	rd = int(omemory[k][16:20],2)
	rn = int(omemory[k][12:16],2)
	shift=omemory[k][25:27]

	s = omemory[k][11]

	cond=omemory[k][0:4]

	#codition check

	#always(normal processing instruction)
	if cond == '1101': pass
	#eq
	elif cond == '0000':
		if cmptemp == 0: pass
		else: continue
	#ne
	elif cond == '0001':
		if (cmptemp >0)|(cmptemp<0):pass
		else: continue
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

	#processing
	# cmp
	if opcode=='1010':
		if I=='0':	# operand is register
			rm = int(omemory[k][28:32],2)
			
			if omemory[k][20:28] !='00000000':
				amount=int(omemory[k][20:25],2)
				
				# lsl
				if shift=='00':
					result=res[rm]<<amount
					cmptemp = res[rn]-result

				
					
				# asr
				elif shift=='10':
					result=res[rm]>>amount
					cmptemp = res[rn]-result
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
				amount=int(omemory[k][20:25],2)
		
				# lsl
				if shift=='00':
					res[rd]=res[rm]<<amount

					flag[rd] = '0'

				# lsr
				elif shift=='01':
					temb= bin(res[rm]).lstrip('0b')
					temb=temb.zfill(8)
					tema= temb[:len(temb)-amount]
					res[rd]=tema.zfill(8)
					
					flag[rd] = '1'
				
				# asr
				elif shift=='10':
					res[rd]=res[rm]>>amount
					
					flag[rd] = '0'
				
				# ror
				elif shift=='11':
					temt= bin(res[rm]).lstrip('0b')
					temt=temt.zfill(8)
					tema= temt[:len(temt)-amount]
					temb=temt[len(temt)-amount:]
					res[rd]=temb+tema

					flag[rd] = '1'
			else:
				
				res[rd]=res[rm]

				flag[rd] = '0'

		else:		# operand is integer
			operand = int(omemory[k][24:32],2)
			res[rd] = operand
	
			flag[rd] = '0'
		
	# add
	elif opcode=='0100':
		if I=='0':	# operand is register
			rm = int(omemory[k][28:32],2)
			
			if omemory[k][20:28] !='00000000':
				amount=int(omemory[k][20:25],2)
				
				# lsl
				if shift=='00':
					result=res[rm]<<amount
					res[rd]=result+res[rn]

					flag[rd] = '0'
					
				# asr
				elif shift=='10':
					result=res[rm]>>amount
					res[rd]=result+res[rn]

					flag[rd] = '0'
			else:
				res[rd]=res[rm]+res[rn]
				
				flag[rd] = '0'

		else:		# operand is integer
			operand = int(omemory[k][24:32],2)
			res[rd] = operand+rn
	
			flag[rd] = '0'


	# sub
	elif opcode=='0010':
		if I=='0':	# operand is register
			rm = int(omemory[k][28:32],2)
			
			if omemory[k][20:28] !='00000000':
				amount=int(omemory[k][20:25],2)
				
				# lsl
				if shift=='00':
					result=res[rm]<<amount
					res[rd]=res[rn]-result

					flag[rd] = '0'
					
				# asr
				elif shift=='10':
					result=res[rm]>>amount
					res[rd]=res[rn]-result

					flag[rd] = '0'
			else:
				res[rd]=res[rn]-res[rm]
				flag[rd] = '0'

		else:		# operand is integer
			operand = int(omemory[k][24:32],2)
			res[rd] = res[rn]-operand
	
			flag[rd] = '0'

	# rsb
	elif opcode=='0011':
		if I=='0':	# operand is register
			rm = int(omemory[k][28:32],2)
			
			if omemory[k][20:28] !='00000000':
				amount=int(omemory[k][20:25],2)
				
				# lsl
				if shift=='00':
					result=res[rm]<<amount
					res[rd]=result-res[rn]

					flag[rd] = '0'
					
				# asr
				elif shift=='10':
					result=res[rm]>>amount
					res[rd]=result-res[rn]

					flag[rd] = '0'
			else:
				res[rd]=res[rm]-res[rn]
				flag[rd] = '0'

		else:		# operand is integer
			operand = int(omemory[k][24:32],2)
			res[rd] = operand-res[rn]
	
			flag[rd] = '0'
	

	# swi
	elif opcode=='1000':
		n=15
		res[n] = (int(k,16)+ 8)

		flag[n] = '0'



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
print cmptemp

for i in range(len(showlist)):
	if flag[i][0]=='0':	
		print '%-8s' % showlist[i],'%0.8x' % reg[i][1]
	else:
		print '%-8s' % showlist[i], reg[i][1]	

