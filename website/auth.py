from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from . import db
from .models import User

#Blueprint
auth = Blueprint('auth', __name__)

#Login Route
@auth.route('/login',methods=['GET','POST'])
def login():
	if request.method=='POST':
		#Get form data
		email = request.form.get('email')
		password = request.form.get('password')
		#Query in Database
		user = User.query.filter_by(email=email).first()
		
		if user:
			if check_password_hash(user.password, password):
				flash('Logged in successfully',category='success') #message flash
				login_user(user,remember=True) #user login and session cookie
				return redirect(url_for('views.home'))
			else:
				flash('Incorrect password.',category='error')
		else:
			flash('Incorrect email.',category='error')
	return render_template("login.html",user=current_user) #rendering page and sending current user to the frontend

@auth.route('/logout')
@login_required
def logout():
	logout_user() #remove session cookie and logout
	return redirect(url_for('auth.login'))

@auth.route('/sign-up',methods=['GET','POST'])
def sign_up():
	if request.method == 'POST':
		email = request.form.get('email')
		firstName = request.form.get('firstName')
		password1 = request.form.get('password1')
		password2 = request.form.get('password2')
		user = User.query.filter_by(email=email).first()
		if user:
			flash('User already exists.',category='error')
		elif len(email)<4:
			flash('Email must be greater than 3 characters.',category='error')
		elif len(firstName)<2:
			flash('First Name must be greater than 1 characters.',category='error')
		elif password1!=password2:
			flash('Passwords do not match.',category='error')
		elif len(password1)<7:
			flash('Password must be at least 7 characters.',category='error')
		else:
			new_user = User(email=email,first_name=firstName,password=generate_password_hash(password1, method='sha256')) #creating an instance of a User Model with form details
			#adding to the database
			db.session.add(new_user)
			db.session.commit()
			login_user(new_user,remember=True) #user login and session cookie
			flash('Account created!')
			return redirect(url_for('views.home'))
	return render_template("signup.html",user=current_user)

@auth.route('/delete-user',methods=['POST'])
@login_required
def deleteUser():
	#removing current user account from database
	db.session.delete(current_user)
	db.session.commit()
	flash('Deleted Account',category='success')
	logout_user() #removing session cookie and logout
	return jsonify({})