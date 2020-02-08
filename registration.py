from datetime import date
import request
import pymysql
from flask import *  
from flask_mail import *  
from random import *    

app = Flask(__name__)  
mail = Mail(app)  
app.secret_key = "abc"  

  
app.config["MAIL_SERVER"]='smtp.gmail.com'  
app.config["MAIL_PORT"] = 465     
app.config["MAIL_USERNAME"] = 'senderMail@gmail.com'  
app.config['MAIL_PASSWORD'] = 'senderMailPassword'  
app.config['MAIL_USE_TLS'] = False  
app.config['MAIL_USE_SSL'] = True  
  
mail = Mail(app)  
otp = randint(000000,999999)  

 
@app.route('/')  
def index():  
	return render_template("index.html")  

 
@app.route('/verify',methods = ["POST","GET"])  
def verify():
	fname = request.form['firstname']
	lname = request.form['lastname']
	email = request.form['mailid']
	mobile = request.form['mobile']
	ap = request.form['pass']

	#email validation

	host = "localhost"
	user = "akshaypawar"
	password = "Appa9596@"
	db = "mydb"
	con = pymysql.Connection(host=host, user=user, password=password, database=db)
	cur = con.cursor()
	query = "select email from registrationapp"
	cur.execute(query)
	rows = cur.fetchall()
	con.commit()
	con.close()
	for row in rows:
		if row[0]==email:
			return "<h1>EMAIL ALREADY USED...</h1>"

	session['fname'] = fname
	session['lname'] = lname
	session['email'] = email
	session['mobile'] = mobile
	session['ap'] = ap


	try:
		msg = Message('OTP',sender = 'senderMail@gmail.com', recipients = [email])
		msg.body = str(otp)
		mail.send(msg)
		return render_template('verify.html')
	except:
		return"<h1>Check your Email Id</h1>"


@app.route('/validate',methods=["POST","GET"])  
def validate():
	fname = session.get('fname', None)
	lname = session.get('lname', None)
	email = session.get('email', None)
	mobile = session.get('mobile', None)
	ap = session.get('ap', None)

	user_otp = request.form['otp']
	if otp == int(user_otp):
		host="localhost"
		user="akshaypawar" 
		password="Appa9596@" 
		db="mydb"
		con = pymysql.Connection(host=host,user=user,password=password,database=db) 
		cur = con.cursor() 

		#for unique token
		
		totalno=0
		f = fname[:2]
		l = lname[:2]
		name = f+l
		for i in name:
        		totalno+=ord(i)
		totalno = str(totalno)
		id = mobile
		no = id[-3:]
		final = totalno+no
		no = int(final)
		token = hex(no)
		msg = Message('TOKEN',sender = 'senderMail@gmail.com', recipients = [email])
		msg.body = str(token)  
		mail.send(msg)  

		#date
		today = date.today()
		dt = today.strftime("%d.%m.%Y")


		q="INSERT INTO registrationapp(firstname,lastname,email,mobile,password,signdate,token) values(%s, %s, %s, %s, %s, %s, %s)"
		cur.execute(q,(fname,lname,email,mobile,ap,dt,token))
		con.commit()
		con.close()
		return "<h3>Registration successfully</h3>"  
	return "<h3>Email verification failed</h3>"

 
if __name__ == '__main__':
	app.run(debug=True)

