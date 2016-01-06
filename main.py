from flask import Flask, request, render_template, url_for, flash, redirect, session,make_response,jsonify
from functools import wraps,update_wrapper
import subprocess
from subprocess import *

app = Flask(__name__, static_url_path='')
app.secret_key="secret"

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route("/")
def home():
	title="Mahabharata"
	return render_template('index.html',title=title)



@app.route("/c_vs_c",methods=['GET','POST'])
def bot():
	error=None;
	if (request.method=='POST'):
		p1=request.form['p1']
		p2=request.form['p2']
		p1f=request.form['p1f']
		p2f=request.form['p2f']
		ext1=p1f.split('.')
		ext2=p2f.split('.')
		session['p1']=p1
		session['p2']=p2
		session['p1f']=p1f
		session['p2f']=p2f
		session['ext1']=ext1[1]
		session['ext2']=ext2[1]	#Best way is by session - Done bit baseless in AHA3d project
		return redirect(url_for('game'))
	return render_template('c_vs_c.html')

@app.route("/game",methods=['GET','POST'])
def game():
	p1=session['p1']
	p2=session['p2']
	p1f=session['p1f']
	p2f=session['p2f']
	ext1=session['ext1']
	ext2=session['ext2']
	return render_template('game.html',p1=p1,p2=p2,p1f=p1f,p2f=p2f,ext1=ext1,ext2=ext2)
	
def check(i,j):
	if i>10 or i<0:
		return 0
	if j>10 or j<0:
		return 0
	return 1

def dfs(i,j,lst):
	if lst[i][j] == -1:
		lst[i][j]==100
		print "Blue Won"
		
	lst[i][j]=10
	if check(i+1,j):
		if lst[i+1][j]==1 or lst[i+1][j]==-1:
			dfs(i+1,j,lst)
	if check(i-1,j):
		if lst[i-1][j]==1 or lst[i-1][j]==-1:
			dfs(i-1,j,lst)
	if check(i,j+1):
		if lst[i][j+1]==1 or lst[i][j+1]==-1:
			dfs(i,j+1,lst)
	if check(i,j-1):
		if lst[i][j-1]==1 or lst[i][j-1]==-1:
			dfs(i,j-1,lst)
	if check(i-1,j+1):
		if lst[i-1][j+1]==1 or lst[i-1][j+1]==-1:
			dfs(i-1,j+1,lst)
	if check(i+1,j-1):
		if lst[i+1][j-1]==1 or lst[i+1][j-1]==-1:
			dfs(i+1,j-1,lst)

def check_blue():
	fob=open('board_file.txt','r')
	list1=[]
	list1=fob.readlines()
	fob.close()
	lst=[]
	for i in range(0,11):
		list_tmp=[]
		for j in range(i*11+1,i*11+12):
			if list1[j].find("B")!=-1 and i!=10:
				list_tmp.append(1)
			elif list1[j].find("B")!=-1 and i==10:
				list_tmp.append(-1)

			else:
				list_tmp.append(0)
				
		lst.append(list_tmp)
	
	for i in range(0,11):
		if lst[0][i]==1:
			dfs(0,i,lst)
			
	for i in range(0,11):
		if lst[10][i]==10:
			return 1
	return 0



@app.route("/red_turn", methods=['GET', 'POST'])
def red():
	file_name = request.args.get('file_name')
	extension = request.args.get('extension')
	fob=open('board_file.txt','r')
	list1=[]
	list1=fob.readlines()
	#*******************************CHECK FOR FILE CHANGE ----MAKE FUNCTION---Partially working----make file readonly!!
	if extension=="cpp":
		first="g++"
		#call([first,file_name,"-o","red"])#***********************check and optimise it../?????????????????CHECK WHEN U WILL CALL THE FILE AND MAKE OPJECT FILE
		output=check_output("./red")
	elif extension=="py":
		first="python"
		output=check_output([first,file_name])
		output = output[:-1]
	#elif extension=="java":
		#***********************MAKE FOR JAVA ALSO
	fob1=open('board_file.txt','r')
	#*************************Check if we get any compilation error or while loop
	output=output+" "
	list2=[]
	list2=fob1.readlines()
	file_changed=0
	wrong_selected=0
	flag=0
	for i in range(0,122):
		if list1[i]!=list2[i]:
			file_changed=1
			break
	for i in range(1,122):
		if list1[i].find(output)!=-1:
			if list1[i].find("U")==-1:
				wrong_selected=1
			list1[i]=list1[i].replace("U","R")
			flag=1
	list1[0]="0\n"
	fob1.close()
	fob.close()
	fob=open('board_file.txt','w')
	fob.writelines(list1)
	fob.close()
	#***************CHECK FOR FILE CHANGE--------------Partially Done
	#***************Check if he has won - IF YES, Then make win variable =1;
	win=0#Change it later
	output = output[:-1]
	data={"win":win,"output":output,"file_changed":file_changed,"wrong_selected":wrong_selected,"flag":flag}
	return jsonify(data)

@app.route("/blue_turn", methods=['GET', 'POST'])
def blue():
	file_name = request.args.get('file_name')
	extension = request.args.get('extension')
	fob=open('board_file.txt','r')
	list1=[]
	list1=fob.readlines()
	#*******************************CHECK FOR FILE CHANGE ----MAKE FUNCTION
	if extension=="cpp":
		first="g++"
		#call([first,file_name,"-o","blue"])
		output=check_output("./blue")
	elif extension=="py":
		first="python"
		output=check_output([first,file_name])
		output = output[:-1]
	#elif extension=="java":
		#***********************MAKE FOR JAVA ALSO
	#***************CHECK FOR FILE CHANGE
	#***************Check if he has won - IF YES, Then make win variable =1;
	#***************UPDATE FILE. CHange 1 to 0 and output element to Red
	fob1=open('board_file.txt','r')
	#*************************Check if we get any compilation error or while loop
	output=output+" "
	list2=[]
	list2=fob1.readlines()
	file_changed=0
	wrong_selected=0
	flag=0
	for i in range(0,122):
		if list1[i]!=list2[i]:
			file_changed=1
			break
	for i in range(1,122):
		if list1[i].find(output)!=-1:
			if list1[i].find("U")==-1:
				wrong_selected=1
			list1[i]=list1[i].replace("U","B")
			flag=1
	list1[0]="1\n"
	fob1.close()
	fob.close()
	fob=open('board_file.txt','w')
	fob.writelines(list1)
	fob.close()
	#***************CHECK FOR FILE CHANGE--------------Partially Done
	win=check_blue()
	#***************Check if he has won - IF YES, Then make win variable =1;-----------TEsting left
	
	output = output[:-1]
	data={"win":win,"output":output,"file_changed":file_changed,"wrong_selected":wrong_selected,"flag":flag}
	return jsonify(data)




if __name__ == "__main__":
	app.run(debug=True)