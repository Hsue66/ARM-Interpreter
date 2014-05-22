import sys

# read input.txt
lines = sys.stdin.readlines()

# read first line as start_point 
start_point = int(lines[0],16)


memory = dict()		# make original input as dict
res = dict()		# make new output as dict
val=[]
count=0
flag=dict()
# read values and address to memory
for l in lines[1:]:
	try:
		[addr,value] = l.split(':')
		memory[addr] = int(value,16)
		
	except:
		pass

# sort
memory=sorted(memory.items(),key=lambda memory:memory[0])
for n in range(len(memory)):
	val.append(memory[n][1])



# change value to binary and strip '0b'
for m in range(len(val)):
	val[m] = bin(val[m]).lstrip('0b')

# write new key(register) and value(result) to res
for n in range(len(val)):
	
	count+=1
	rd=int(val[n][16:20],2)
	rn=int(val[n][12:16],2)

	# mov
	if val[n][7:11] == '1101':
	
		if val[n][6]=='0':
			if val[n][20:28]!='00000000':
				if val[n][27]=='0':
					amount=int(val[n][20:25],2)
					rm=int(val[n][28:32],2)
					# lsl
					if val[n][25:27]=='00':
						result=res[rm]*(2**amount)
						res[rd]=result
						flag[rd] = '0'
					
					# lsr
					elif val[n][25:27]=='01':
			
						temb= bin(res[rm]).lstrip('0b')
						l=8-len(temb)
						zeros="0"*l
						temb=zeros+temb
						tema= temb[:len(temb)-amount]
						l=8-len(tema)
						zeros="0"*l
						res[rd]=zeros+tema
						
						flag[rd] = '1'

					# asr
					elif val[n][25:27]=='10':
						result=res[rm]/(2**amount)
						res[rd]=result
						flag[rd] = '0'
						

					# ror
					elif val[n][25:27]=='11':
				
						temp= bin(res[rm]).lstrip('0b')
						l=8-len(temp)
						zeros="0"*l
						temp=zeros+temp
						print temp

						tema= temp[:len(temp)-amount]
						print tema
						temb=temp[len(temp)-amount:]
						print temb
					
				
						res[rd]=temb+tema
						print res[rd]	
						flag[rd] = '1'

				# rs			
				#else:
					
			else:
				rm=int(val[n][24:32],2)
				res[rd]=res[rm]
				flag[rd] = '0'

		else:
			rm=int(val[n][24:32],2)
			res[rd]=rm
			flag[rd] = '0'


	# add
	elif val[n][7:11]=='0100':
		if val[n][6]=='0':
			if val[n][20:28]!='00000000':
				if val[n][27]=='0':
					amount=int(val[n][20:25],2)
					rm=int(val[n][28:32],2)
					# lsl
					if val[n][25:27]=='00':
						result=res[rm]*(2**amount)
						res[rd]=result+res[rn]
						flag[rd] = '0'

					# lsr
					#elif val[n][25:27]=='01':
			
					#	temb= bin(res[rm]).lstrip('0b')
					#	l=8-len(temb)
					#	zeros="0"*l
					#	temb=zeros+temb
					#	tema= temb[:len(temb)-amount]
					#	l=8-len(tema)
					#	zeros="0"*l
					#	res[rd]=zeros+tema
					#	
					#	flag[rd] = '1'

					# asr
					elif val[n][25:27]=='10':
						result=res[rm]/(2**amount)
						print amount
						print result
						print res[rn]
						res[rd]=result+res[rn]
						flag[rd] = '0'
						

					# ror
					#elif val[n][25:27]=='11':
				
					#	temp= bin(res[rm]).lstrip('0b')
					#	l=8-len(temp)
					#	zeros="0"*l
					#	temp=zeros+temp
					#	print temp

					#	tema= temp[:len(temp)-amount]
					#	print tema
					#	temb=temp[len(temp)-amount:]
					#	print temb
					
				
					#	res[rd]=temb+tema
					#	print res[rd]	
					#	flag[rd] = '1'

				# rs			
				#else:

			else:
				rm=int(val[n][24:32],2)
				res[rd]=res[rm]+res[rn]	
				flag[rd] = '0'

		else:
			rm=int(val[n][24:32],2)
			res[rd]=res[rn]+rm
			flag[rd] = '0'
	
	else:
		n=15
		flag[n] = '0'
		res[n] = start_point + (count-1)*4+8


reg = res.items()	# make res as list
reg.sort()		# sort res list


# initialize unexist register
for k in range(16):
	if k !=reg[k][0]:
		flag[k] = '0'
		reg.insert(k,(k,0))


# output format
list = ['r0:','r1:','r2:','r3:','r4:','r5:','r6:','r7:','r8:',
	'r9:','r10:','r11:','r12:','r13 sp:','r14 lr:','r15 pc:']

# display registers and values
for i in range(len(list)):
	if flag[i][0] == '0':
		print '%-8s' % list[i],'%0.8x' % reg[i][1]
	else:
		print '%-8s' % list[i], reg[i][1]

