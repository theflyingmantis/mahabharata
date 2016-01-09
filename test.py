fob=open("board_file.txt",'r')
list1=[]
list1=fob.readlines()
for i in range(1,122):
	words=list1[i].split()
	if words[1]=="U":
		print words[0]
		fob.close()
		# fob=open("board_file",'w')
		# fob.writelines(words)
		# fob.close()
		break

