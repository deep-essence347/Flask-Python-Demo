from os import path

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy()
DB_NAME='database.db'

def create_app():
	#Flask and DB config
	app = Flask(__name__)
	app.config['SECRET_KEY'] = 'fagsdfbaisdfkbdjkgn'
	app.config['SQLALCHEMY_DATABASE_URI']=f'sqlite:///{DB_NAME}'
	db.init_app(app)

	from .auth import auth
	from .views import views

	#setting initial routes
	app.register_blueprint(auth,url_prefix='/')
	app.register_blueprint(views,url_prefix='/')

	from .models import Note, User

	#creating a database
	with app.app_context():
		db.create_all()
		
	login_manager = LoginManager()
	login_manager.login_view = 'auth.login' #if the user is not logged in, redirects to login page
	login_manager.init_app(app)

	#Loading a user
	@login_manager.user_loader
	def load_user(id):
		return User.query.get(int(id))

	return app
