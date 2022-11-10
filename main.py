from website import create_app

#creating a web-application with the files in /website

app = create_app()

if __name__ == '__main__':
	app.run(debug=True)