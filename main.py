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
	
@app.route("/red_turn", methods=['GET', 'POST'])
def red():
	file_name = request.args.get('file_name')
	extension = request.args.get('extension')
	#*******************************CHECK FOR FILE CHANGE ----MAKE FUNCTION
	if extension=="cpp":
		first="g++"
		call([first,file_name,"-o","red"])
		output=check_output("./red")
	elif extension=="py":
		first="python"
		#******************************MAKE FOR PYTHON - CHECK FIRST - HOW TO TAKE OUTPUT
	#elif extension=="java":
		#***********************MAKE FOR JAVA ALSO
	#***************CHECK FOR FILE CHANGE
	#***************Check if he has won - IF YES, Then make win variable =1;
	#***************UPDATE FILE. CHange 1 to 0 and output element to Red
	win=0#Change it later
	data={"win":win,"output":output}
	return jsonify(data)

@app.route("/blue_turn", methods=['GET', 'POST'])
def blue():
	file_name = request.args.get('file_name')
	extension = request.args.get('extension')
	#*******************************CHECK FOR FILE CHANGE ----MAKE FUNCTION
	if extension=="cpp":
		first="g++"
		call([first,file_name,"-o","blue"])
		output=check_output("./blue")
	elif extension=="py":
		first="python"
		#******************************MAKE FOR PYTHON - CHECK FIRST - HOW TO TAKE OUTPUT
	#elif extension=="java":
		#***********************MAKE FOR JAVA ALSO
	#***************CHECK FOR FILE CHANGE
	#***************Check if he has won - IF YES, Then make win variable =1;
	#***************UPDATE FILE. CHange 1 to 0 and output element to Red
	win=0#change it later
	data={"win":win,"output":output}
	return jsonify(data)




if __name__ == "__main__":
	app.run(debug=True)