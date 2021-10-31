from flask import Flask, render_template

app = Flask(__name__)


@app.route("/signup")
def signup():
	return render_template("signup_form.html")

app.run()
