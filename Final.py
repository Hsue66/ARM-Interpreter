# SYSTEM PROGRAMMING TERM PROJECT #

import sys
import collections


# shift operation function #
def do_shift(rd,shift,k):
	# shift count value	
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


# accumulate memory function #
def accumulate_memory(accu,val,addrmemory,byte_word):
	if byte_word == '1':
		addrmemory.pop(accu)				
		addrmemory.insert(accu,(accu,val[6:8]))
		accu+=1

		addrmemory.pop(accu)
		addrmemory.insert(accu,(accu,val[4:6]))
		accu+=1

		addrmemory.pop(accu)
		addrmemory.insert(accu,(accu,val[2:4]))
		accu+=1

		addrmemory.pop(accu)
		addrmemory.insert(accu,(accu,val[0:2]))
		accu+=1
	else:
		addrmemory.pop(accu)				
		addrmemory.insert(accu,(accu,val[6:8]))
		accu+=1
	return addrmemory


memory = dict()		# make original input as dict
res = dict()		# make new output as dict
flag =dict()		# make flag to differenciate string and integer

# list for pushpop
pushlist=list()
poplist=list()
popreglist=list()

imm24=0			# branch offset 24bit integer
cmptemp = 0		# set cmptemp's base value
rn_add = 0		# rd's addresss(in ldr/str)	
k = '0'			# initialize address
store=0			# push amount
push=0			# flag for push

# set CPSR flags
carryflag = 0
overflowflag = 0
zeroflag = 0
negativeflag = 0


# read input.txt
lines = sys.stdin.readlines()


# read first line as start_point 
start_point = int(lines[0],16)


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

# initialize register
for init in range(16):
	if init==13: 		
		# initialize stackpointer
		res[init]=int(omemory.keys()[0],16)-4
		flag[init]='0'
	else:
		res[init] = 0
		flag[init] = '0'



# ldrstr 
temp_index=0
accu=0				# accumulated value
temp_offset = 0
addrmemory=list()		# list to accumulate memory 
addrmemory = [(0,'00')]*100000
indexmemory=list()		# about accumulated index



# write new key(register) and value(result) to res
while(1):

	if k == '0':	# if k=0, make start_point as start address
		k = hex(start_point).lstrip('0x')
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
		if zeroflag == 1: pass
		else: continue
	#ne
	elif cond == '0001':
		if ~(zeroflag == 1): pass
		else: continue
	#ge
	elif cond == '1010':
		if zeroflag == 1 or negativeflag == 0 : pass
		else: continue
	#le
	elif cond == '1101':
		if zeroflag == 1 or negativeflag == 1 : pass
		else: continue
	#gt
	elif cond == '1100':
		if zeroflag == 0 and negativeflag == 0 : pass
		else: continue
	#lt
	elif cond == '1011':
		if zeroflag == 0 and negativeflag == 1 : pass
		else: continue
	
	else: pass


	#Bx lr
	if omemory[k][8:] == '001011111111111100011110':
		if flag[14] == '1':
			k = hex(int(res[14],16)+4).lstrip('0x')
		else:
			k = hex(res[14]+4).lstrip('0x')
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
			res[14] = k.zfill(8)			# set load register 
			flag[14] = '1'

			if push==1:
				pushlist[0]=(pushlist[0][0],res[14])	# update lr of pushlist

			# branch offset +
			if omemory[k][8] == '0':
				imm24 = int(omemory[k][8:],2)
				k = hex(imm24*4 + 8 + int(k,16)).lstrip('0x')

			# branch offset - 2's complement
			else:
				imm24 = int(omemory[k][8:],2)
				imm24 = int(bin((~imm24+1)&0xFF).lstrip('0b'),2)
				k= hex(-imm24*4 + 8 + int(k,16)).lstrip('0x')


	# seperate omemory each part
	I=omemory[k][6]		
	opcode = omemory[k][7:11]
	rd = int(omemory[k][16:20],2)
	rn = int(omemory[k][12:16],2)
	shift=omemory[k][25:27]
	sdt = omemory[k][4:6]
	pushpop=omemory[k][4:7]
	


	# processing #
	# cmp
	if opcode=='1010' and sdt != '01':
		cmptemp = 0
		carryflag = 0
		overflowflag = 0
		zeroflag = 0
		negativeflag = 0

		if I=='0':	# operand is register
			rm = int(omemory[k][28:32],2)
			
			if omemory[k][20:28] !='00000000':
				cmptemp=res[rn]-do_shift(rd,shift,k)
				if cmptemp > 255:
					if res[rn] > 0 and do_shift(rd,shift,k) > 0:
						carryflag = 1
				elif cmptemp > 127:
					if res[rn] < 0 or do_shift(rd,shift,k) < 0:
						overflowflag = 1
				elif cmptemp < 0:
					negativeflag = 1
				elif cmptemp == 0:
					zeroflag = 1
				else: pass
			else:
				cmptemp = res[rn]-res[rm]
				if cmptemp > 255:
					if res[rn] > 0 and res[rm] > 0:
						carryflag = 1
				elif cmptemp > 127:
					if res[rn] < 0 or res[rm] < 0:
						overflowflag = 1
				elif cmptemp < 0:
					negativeflag = 1
				elif cmptemp == 0:
					zeroflag = 1
				else: pass

		else:		# operand is integer
			operand = int(omemory[k][24:32],2)
		
			cmptemp = res[rn]-operand
			if cmptemp > 255:
				if res[rn] > 0 and operand > 0:
					carryflag = 1
			elif cmptemp > 127:
				if res[rn] < 0 or operand < 0:
					overflowflag = 1
			elif cmptemp < 0:
				negativeflag = 1
			elif cmptemp == 0:
				zeroflag = 1
			else: pass

	# pushpop
	if pushpop=='100':
		registerlist=omemory[k][16:32]
		
		# store to memory
		if omemory[k][11]=='0': 
			push=1
			for a in range(len(registerlist)):
				if registerlist[a]=='1':
					store +=1
					# make list with stack_pointer and register_value
					pushlist.append((res[rn]-4*(store-1),res[15-a]))
			
		# load from memory
		else:
			# if pop{pc} : break 
			if registerlist[0]=='1':	
				res[15]=(int(k,16)+ 8)
				break
			
			# make pop register list
			for a in range(len(registerlist)):
				if registerlist[a]=='1':
					popreglist.append(15-a)
		
			popreglist.sort()
	
			# pop		
			for i in popreglist:	
				poplist=pushlist.pop()
				res[13]=poplist[0]	# pop stack_pointer
				res[i]=poplist[1]	# pop register_value
	
	inst=omemory[k][4:6]

	# seperate by inst 01 
	if inst=='01':
		strldr=omemory[k][7:12]
		rn=int(omemory[k][12:16],2)
		rd=int(omemory[k][16:20],2)
		offset=int(omemory[k][20:32],2)

		pre_post = omemory[k][7] 	# pre : add offsetbefore transfer post : add offset after transfer
		up_down = omemory[k][8]		# up : add offset Down : sub offset
		byte_word = omemory[k][9]	# byte / word quantity
		write_back = omemory[k][10]	# write address into base
		load_store_bit = omemory[k][11]	# load/store flag 

		if I == '0':
			if pre_post == '0':
				if byte_word == '0':
					#STR
					if load_store_bit == '0':
						val=(hex(res[rd]).lstrip('0x')).zfill(8)

						indexmemory.append((rn+res[rn],accu))	

						accumulate_memory(accu,val,addrmemory,byte_word)
						accu=0

						if offset != 0:
							accu = offset
						else:
							if up_down == '1':
								accu+=res[rn]
							else:
								accu-=res[rn]

						for inmemo in range(len(indexmemory)-1):
							indexmemory.pop()
					#LDR
					elif load_store_bit == '1':	
						index=0
						out=""
						outmemory=list()
						for i in range(len(indexmemory)):
							if indexmemory[i][0]==rn:
								index=indexmemory[i][1]

						if up_down == '1':
							index+=temp_index
						else:
							index-=temp_index

						for i in range(4):	
							outmemory.append(addrmemory[index][1])
							index-=1

						if offset !=0:
							if up_down == '1':
								temp_index = index + offset
							else:
								temp_index = index + offset
						outmemory.reverse()
						res[rd]=int(out.join(outmemory),16)
				elif byte_word == '1':
					#STR
					if load_store_bit == '0':
						val=(hex(res[rd]).lstrip('0x')).zfill(8)

						indexmemory.append((rn+res[rn],accu))	

						accumulate_memory(accu,val,addrmemory,byte_word)
						accu=0

						if offset != 0:
							accu = offset
						else:
							if up_down == '1':
								accu+=res[rn]
							else:
								accu-=res[rn]

						for inmemo in range(len(indexmemory)-1):
							indexmemory.pop()
					#LDR
					elif load_store_bit == '1':
								
						index=0
						out=""
						outmemory=list()
						for i in range(len(indexmemory)):
							if indexmemory[i][0]==rn:
								index=indexmemory[i][1]
						if up_down == '1':
							index+=temp_index
						else:
							index-=temp_index
						
						outmemory.append(addrmemory[index][1])

						if offset !=0:
							if up_down == '1':
								temp_index = index + offset
							else:
								temp_index = index + offset

						outmemory.reverse()
						res[rd]=int(out.join(outmemory),16)
		
			elif pre_post == '1':
				if byte_word == '0':
					#STR
					if load_store_bit == '0':
						val=(hex(res[rd]).lstrip('0x')).zfill(8)
			
						if offset != 0:
							accu = offset
						else:
							if up_down == '1':
								accu+=res[rn]
							else:
								accu-=res[rn]

						indexmemory.append((rn+res[rn],accu))	

						accumulate_memory(accu,val,addrmemory,byte_word)
								
						if write_back == '0':
							accu=0		
								
				
						for inmemo in range(len(indexmemory)-1):
							indexmemory.pop()
					#LDR
					elif load_store_bit == '1':
						index=0
						out=""
						outmemory=list()
						for i in range(len(indexmemory)):
							if indexmemory[i][0]==rn:
								index=indexmemory[i][1]

						if offset !=0:
							if up_down == '1':
								index += offset
							else:
								index -= offset
						else:
							if write_back == '0':
								index = 0

						for i in range(4):	
							outmemory.append(addrmemory[index][1])
							index-=1

						outmemory.reverse()
						res[rd]=int(out.join(outmemory),16)
				elif byte_word == '1':
					#STR
					if load_store_bit == '0':
						val=(hex(res[rd]).lstrip('0x')).zfill(8)
			
						if offset != 0:
							accu = offset
						else:
							if up_down == '1':
								accu+=res[rn]
							else:
								accu-=res[rn]

						indexmemory.append((rn+res[rn],accu))

						accumulate_memory(accu,val,addrmemory,byte_word)	
					
						if write_back == '0':
							accu=0

						for inmemo in range(len(indexmemory)-1):
							indexmemory.pop()
					#LDR
					elif load_store_bit == '1':
						index=0
						out=""
						outmemory=list()
						for i in range(len(indexmemory)):
							if indexmemory[i][0]==rn:
								index=indexmemory[i][1]

						if offset !=0:
							if up_down == '1':
								index += offset
							else:
								index -= offset
						else:
							if write_back == '0':
								index = 0

						outmemory.append(addrmemory[index][1])
						index-=1

						outmemory.reverse()
						res[rd]=int(out.join(outmemory),16)
	# seperate by inst 00 
	if inst=='00':
		# mov
		if opcode=='1101':
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
				carryflag = 0
				overflowflag =0
				zeroflag = 0
				negativeflag = 0
				cmptemp = res[rd]
				if cmptemp > 255:
					if res[rm] > 0 and res[rs] > 0:
						carryflag = 1
				elif cmptemp > 127:
					if res[rm] < 0 or res[rs] < 0:
						overflowflag = 1
				elif cmptemp < 0:
					negativeflag = 1
				elif cmptemp == 0:
					zeroflag = 1
				else: pass
		
			flag[rd]='0'

		# add
		elif opcode=='0100':
			if I=='0':	# operand is register
				rm = int(omemory[k][28:32],2)
			
				if omemory[k][20:28] !='00000000':
					res[rd]=do_shift(rd,shift,k)+res[rn]
					if S =='1':
						carryflag = 0
						overflowflag = 0
						zeroflag = 0
						negativeflag = 0
						if res[rd] > 255:
							if res[rn] > 0 and do_shift(rd,shift,k) > 0:
								carryflag = 1
						elif res[rd] > 127:
							if res[rn] < 0 or do_shift(rd,shift,k) < 0:
								overflowflag = 1
						elif res[rd] < 0:
							negativeflag = 1
						elif res[rd] == 0:
							zeroflag = 1
						else: pass

					flag[rd] = '0'
				else:
					res[rd]=res[rm]+res[rn]
                        	        if S =='1':
						carryflag = 0
						overflowflag = 0
						zeroflag = 0
						negativeflag = 0
						if res[rd] > 255:
							if res[rn] > 0 and res[rm] > 0:
								carryflag = 1
						elif res[rd] > 127:
							if res[rn] < 0 or res[rm] < 0:
								overflowflag = 1
						elif res[rd] < 0:
							negativeflag = 1
						elif res[rd] == 0:
							zeroflag = 1
						else: pass
				
					flag[rd] = '0'

			else:		# operand is integer
				operand = int(omemory[k][24:32],2)
				res[rd] = operand+res[rn]
        	                if S =='1':
					carryflag = 0
					overflowflag = 0
					zeroflag = 0
					negativeflag = 0
					if res[rd] > 255:
						if res[rn] > 0 and operand > 0:
							carryflag = 1
					elif res[rd] > 127:
						if res[rn] < 0 or operand < 0:
							overflowflag = 1
					elif res[rd] < 0:
						negativeflag = 1
					elif res[rd] == 0:
						zeroflag = 1
					else: pass
		
				flag[rd] = '0'


		# sub
		elif opcode=='0010':
			if I=='0':	# operand is register
				rm = int(omemory[k][28:32],2)
				
				if omemory[k][20:28] !='00000000':
					res[rd]=res[rn]-do_shift(rd,shift,k)
					if S == '1':
						carryflag = 0
						overflowflag = 0
						zeroflag = 0
						negativeflag = 0
						if res[rd] > 255:
							if res[rn] > 0 and do_shift(rd,shift,k) > 0:
								carryflag = 1
						elif res[rd] > 127:
							if res[rn] < 0 or do_shift(rd,shift,k) < 0:
								overflowflag = 1
						elif res[rd] < 0:
							negativeflag = 1
						elif res[rd] == 0:
							zeroflag = 1
						else: pass
					
						flag[rd] = '0'
				else:
					res[rd]=res[rn]-res[rm]
					if S == '1':
						carryflag = 0
						overflowflag = 0
						zeroflag = 0
						negativeflag = 0
						if res[rd] > 255:
							if res[rn] > 0 and res[rm] > 0:
								carryflag = 1
						elif res[rd] > 127:
							if res[rn] < 0 or res[rm] < 0:
								overflowflag = 1
						elif res[rd] < 0:
							negativeflag = 1
						elif res[rd] == 0:
							zeroflag = 1
						else: pass
				
					flag[rd] = '0'
	
			else:		# operand is integer
				operand = int(omemory[k][24:32],2)
				res[rd] = res[rn]-operand
				if S == '1':
					carryflag = 0
					overflowflag = 0
					zeroflag = 0
					negativeflag = 0
					if res[rd] > 255:
						if res[rn] > 0 and operand > 0:
							carryflag = 1
					elif res[rd] > 127:
						if res[rn] < 0 or operand < 0:
							overflowflag = 1
					elif res[rd] < 0:
						negativeflag = 1
					elif res[rd] == 0:
						zeroflag = 1
					else: pass
			
				flag[rd] = '0'

		# rsb
		elif opcode=='0011':
			if I=='0':	# operand is register
				rm = int(omemory[k][28:32],2)
			
				if omemory[k][20:28] !='00000000':
					res[rd]=do_shift(rd,shift,k)-res[rn]
					if S =='1':
						carryflag = 0
						overflowflag = 0
						zeroflag = 0
						negativeflag = 0
						if res[rd] > 255:
							if res[rn] > 0 and do_shift(rd,shift,k) > 0:
								carryflag = 1
						elif res[rd] > 127:
							if res[rn] < 0 or do_shift(rd,shift,k) < 0:
								overflowflag = 1
						elif res[rd] < 0:
							negativeflag = 1
						elif res[rd] == 0:
							zeroflag = 1
						else: pass
	
					flag[rd] = '0'
				else:
					res[rd]=res[rm]-res[rn]
					if S =='1':
						carryflag = 0
						overflowflag = 0
						zeroflag = 0
						negativeflag = 0
						if res[rd] > 255:
							if res[rn] > 0 and res[rm] > 0:
								carryflag = 1
						elif res[rd] > 127:
							if res[rn] < 0 or res[rm] < 0:
								overflowflag = 1
						elif res[rd] < 0:
							negativeflag = 1
						elif res[rd] == 0:
							zeroflag = 1
						else: pass
					flag[rd] = '0'
	
			else:		# operand is integer
				operand = int(omemory[k][24:32],2)
				res[rd] = operand-res[rn]
	                        if S =='1':
					carryflag = 0
					overflowflag = 0
					zeroflag = 0
					negativeflag = 0
					if res[rd] > 255:
						if res[rn] > 0 and operand > 0:
							carryflag = 1
					elif res[rd] > 127:
						if res[rn] < 0 or operand < 0:
							overflowflag = 1
					elif res[rd] < 0:
						negativeflag = 1
					elif res[rd] == 0:
						zeroflag = 1
					else: pass
	
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
	

	
reg = res.items()	# make res as list

# output format
showlist = ['r0:','r1:','r2:','r3:','r4:','r5:','r6:','r7:','r8:',
	'r9:','r10:','r11:','r12:','r13 sp:','r14 lr:','r15 pc:']

# display registers and values
for i in range(len(showlist)):
	if flag[i][0]=='0':	
		print '%-8s' % showlist[i],'%0.8x' % reg[i][1]
	else:
		print '%-8s' % showlist[i], reg[i][1]
