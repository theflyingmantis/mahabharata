fob=open('board_file.txt','w')
list1 = []
list1.append('1\n')
for i in range(0,11):
	for j in range(1,12):
		a=chr(i+ord('A'))
		a=a+str(j)
		a=a+" U\n"
		list1.append(a)
fob.writelines(list1)
fob.close()