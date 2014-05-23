import sys

# read input.txt
lines = sys.stdin.readlines()

# read first line as start_point 
start_point = int(lines[0],16)


memory = dict()		# make original input as dict
res = dict()		# make new output as dict
val=[]

count=0
flag =dict()
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
	temp = []
	tem_rm = []
	tem = []
	count+=1
	rd=int(val[n][16:20],2)
	rn=int(val[n][12:16],2)

	# mov
	if val[n][7:11] == '1101':
		if val[n][6]=='0':
			rm=int(val[n][24:32],2)
			res[rd]=res[rm]	
		else:
			rm=int(val[n][24:32],2)
			res[rd]=rm
		flag[rd] = '0'
	# add
	elif val[n][7:11]=='0100':
		
		if val[n][6]=='0':
			rm=int(val[n][24:32],2)
			res[rd]=res[rm]+res[rn]	
		else:
			rm=int(val[n][24:32],2)
			res[rd]=res[rn]+rm
		flag[rd] = '0'
	# sub
	elif val[n][7:11]=='0010':
		if val[n][6]=='0':
			rm=int(val[n][24:32],2)
			res[rd]=res[rn]-res[rm]
		else:
			rm=int(val[n][24:32],2)
			res[rd]=res[rn]-rm
		flag[rd] = '0'
	# rsb
	elif val[n][7:11]=='0011':
		if val[n][6]=='0':
			rm=int(val[n][24:32],2)
			res[rd]=res[rm]-res[rn]	
		else:
			rm=int(val[n][24:32],2)
			res[rd]=rm-res[rn]
		flag[rd] = '0'
	#eor
	elif val[n][7:11] == '0001':
		tem_rn = val[rn][24:32]
		
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
		tem_rn = val[rn][24:32]

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
		tem_rn = val[rn][24:32]
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
		tem_rn = val[rn][24:32]
		tem_rm = val[n][24:32]

		for k in range(len(tem_rn)):
			if tem_rm[k] == '0':
				temp.append(1)
			else:
				temp.append(0)
		temp =''.join(map(str,temp))
		for k in range(len(tem_rn)):
			if tem_rn[k] == '0' and temp == '0':
				tem.append(0);
			else:
				tem.append(1);
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


