import sys

# read input.txt
lines = sys.stdin.readlines()

# read first line as start_point 
start_point = int(lines[0],16)


memory = dict()		# make original input as dict
res = dict()		# make new output as dict
val=[]
count=0
flag =dict()		# make flag to differenciate string and integer

# read values and address to memory
for l in lines[1:]:
	try:
		[addr,value] = l.split(':')
		memory[addr] = int(value,16)
		
	except:
		pass

# sort and extract value
memory=sorted(memory.items(),key=lambda memory:memory[0])
for n in range(len(memory)):
	val.append(memory[n][1])

# change value to binary and strip '0b'
for m in range(len(val)):
	val[m] = bin(val[m]).lstrip('0b')
	

# write new key(register) and value(result) to res
for n in range(len(val)):
	temp = []
	tem = []
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
				
						temt= bin(res[rm]).lstrip('0b')
						l=8-len(temt)
						zeros="0"*l
						temt=zeros+temt
						tema= temt[:len(temt)-amount]
						temb=temt[len(temt)-amount:]
						res[rd]=temb+tema
	
						flag[rd] = '1'
					
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
					
					# asr
					elif val[n][25:27]=='10':
						result=res[rm]/(2**amount)
						res[rd]=result+res[rn]

						flag[rd] = '0'
			
			else:
				rm=int(val[n][24:32],2)
				res[rd]=res[rm]+res[rn]	

				flag[rd] = '0'

		else:
			rm=int(val[n][24:32],2)
			res[rd]=res[rn]+rm

			flag[rd] = '0'


	# sub
	elif val[n][7:11]=='0010':
		if val[n][6]=='0':
			if val[n][20:28]!='00000000':
				if val[n][27]=='0':
					amount=int(val[n][20:25],2)
					rm=int(val[n][28:32],2)
					# lsl
					if val[n][25:27]=='00':
						
						result=res[rm]*(2**amount)
						res[rd]=res[rn]-result

						flag[rd] = '0'
					
					# asr
					elif val[n][25:27]=='10':
						result=res[rm]/(2**amount)
						res[rd]=res[rn]-result

						flag[rd] = '0'
			else:
				rm=int(val[n][24:32],2)
				res[rd]=res[rn]-res[rm]
				flag[rd] = '0'

		else:
			rm=int(val[n][24:32],2)
			res[rd]=res[rn]-rm
			flag[rd] = '0'

	# rsb
	elif val[n][7:11]=='0011':
		if val[n][6]=='0':
			if val[n][20:28]!='00000000':
				if val[n][27]=='0':
					amount=int(val[n][20:25],2)
					rm=int(val[n][28:32],2)
					# lsl
					if val[n][25:27]=='00':
						
						result=res[rm]*(2**amount)
						res[rd]=result-res[rn]

						flag[rd] = '0'
					
					# asr
					elif val[n][25:27]=='10':
						result=res[rm]/(2**amount)
						res[rd]=result-res[rn]

						flag[rd] = '0'
			else:
				rm=int(val[n][24:32],2)
				res[rd]=res[rm]-res[rn]
				flag[rd] = '0'

		else:
			rm=int(val[n][24:32],2)
			res[rd]=rm-res[rn]
			flag[rd] = '0'

	#eor
	elif val[n][7:11] == '0001':
		tem_rn = bin(res[rn]).lstrip('0b')
		l=8-len(tem_rn)
		zeros="0"*l
		tem_rn=zeros+tem_rn
		
		if val[n][6] == '0':
			rm=int(val[n][24:32],2)
			tem_rm = bin(res[rm]).lstrip('0b')
			l=8-len(tem_rm)
			zeros="0"*l
			tem_rm=zeros+tem_rm	

			for k in range(len(tem_rn)):
				if tem_rn[k] == tem_rm[k]:
					temp.append(0);
				else:
					temp.append(1);
			temp = ''.join(map(str,temp))
			res[rd] = temp
			flag[rd] = '1'
		else:
			rm=int(val[n][24:32],2)
			tem_rm = bin(rm).lstrip('0b')
			l=8-len(tem_rm)
			zeros="0"*l
			tem_rm=zeros+tem_rm	

			for k in range(len(tem_rn)):
				if tem_rn[k] == tem_rm[k]:
					temp.append(0);
				else:
					temp.append(1);
			temp = ''.join(map(str,temp))
			res[rd] = temp
			flag[rd] = '1'

	#and
	elif val[n][7:11] == '0000':
		tem_rn = bin(res[rn]).lstrip('0b')
		l=8-len(tem_rn)
		zeros="0"*l
		tem_rn=zeros+tem_rn

		if val[n][6] == '0':
			rm=int(val[n][24:32],2)
			tem_rm = bin(res[rm]).lstrip('0b')
			l=8-len(tem_rm)
			zeros="0"*l
			tem_rm=zeros+tem_rm	
			for k in range(len(tem_rn)):
				if tem_rn[k] == '1' and tem_rm[k] == '1':
					temp.append(1);
				else:
					temp.append(0);
			temp = ''.join(map(str,temp))
			res[rd] = temp
			flag[rd] = '1'
		else:
			rm=int(val[n][24:32],2)
			tem_rm = bin(rm).lstrip('0b')
			l=8-len(tem_rm)
			zeros="0"*l
			tem_rm=zeros+tem_rm	
			for k in range(len(tem_rn)):
				if tem_rn[k] == '1' and tem_rm[k] == '1':
					temp.append(1);
				else:
					temp.append(0);
			temp = ''.join(map(str,temp))
			res[rd] = temp
			flag[rd] = '1'
	
	#orr
	elif val[n][7:11] == '1100':
		tem_rn = bin(res[rn]).lstrip('0b')
		l=8-len(tem_rn)
		zeros="0"*l
		tem_rn=zeros+tem_rn
		if val[n][6] == '0':
			rm=int(val[n][24:32],2)
			tem_rm = bin(res[rm]).lstrip('0b')
			l=8-len(tem_rm)
			zeros="0"*l
			tem_rm=zeros+tem_rm	
			for k in range(len(tem_rn)):
				if (tem_rn[k] == '0') and (tem_rm[k] == '0'):
					temp.append(0);
				else:
					temp.append(1);
			temp = ''.join(map(str,temp))
			res[rd] = temp	
			flag[rd] = '1'
		else:
			rm = int(val[n][24:32],2)
			tem_rm = bin(rm).lstrip('0b')
			l=8-len(tem_rm)
			zeros="0"*l
			tem_rm=zeros+tem_rm	
			for k in range(len(tem_rn)):
				if tem_rn[k] == '0' and tem_rm[k] == '0':
					temp.append(0);
				else:
					temp.append(1);
			temp = ''.join(map(str,temp))
			res[rd] = temp	
			flag[rd] = '1'

	#mvn
	elif val[n][7:11] == '1111':
		if val[n][6] == '0':
			rm=int(val[n][24:32],2)
			tem_rm = bin(res[rm]).lstrip('0b')
			l=8-len(tem_rm)
			zeros="0"*l
			tem_rm=zeros+tem_rm	
			for k in range(len(tem_rm)):
				if tem_rm[k] == '0':
					temp.append(1)
				else:
					temp.append(0)
			temp =''.join(map(str,temp))
			res[rd] = temp
			flag[rd] = '1'
		else:
			rm = int(val[n][24:32],2)
			tem_rm = bin(rm).lstrip('0b')
			l=8-len(tem_rm)
			zeros="0"*l
			tem_rm=zeros+tem_rm
			for k in range(len(tem_rm)):
				if tem_rm[k] == '0':
					temp.append(1)
				else:
					temp.append(0)
			temp =''.join(map(str,temp))
			res[rd] = temp
			flag[rd] = '1'

	#bic
	elif val[n][7:11] == '1110':
		tem_rn = bin(res[rn]).lstrip('0b')
		l=8-len(tem_rn)
		zeros="0"*l
		tem_rn=zeros+tem_rn

		rm = int(val[n][24:32],2)
		tem_rm = bin(rm).lstrip('0b')
		l=8-len(tem_rm)
		zeros="0"*l
		tem_rm=zeros+tem_rm

		for k in range(len(tem_rn)):
			if tem_rm[k] == '0':
				temp.append(1)
			else:
				temp.append(0)
		temp =''.join(map(str,temp))
		print temp
		print tem_rn
		for k in range(len(tem_rn)):
			if tem_rn[k] == '1' and temp[k] == '1':
				tem.append(1);
			else:
				tem.append(0);
		tem = ''.join(map(str,tem))
		flag[rd] = '1'
		res[rd] = tem	

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

