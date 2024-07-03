from flask import Flask, render_template, url_for, flash, redirect, request
from forms import RegistrationForm
from flask_behind_proxy import FlaskBehindProxy
import git

app = Flask(__name__)
proxied = FlaskBehindProxy(app)
app.config['SECRET_KEY'] = 'da385b2be3f77cace27d1ab4c1f66ca7'

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", subtitle="Welcome to Get Your Music", text="This is a fun website where you are able to get song recommendations")

@app.route("/register", methods=["GET","POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Your account was created successfully for {form.username.data}!', 'success') 
        return redirect(url_for('home'))
    return render_template("register.html", title="Register", form=form)

@app.route("/update_server", methods=['POST'])
def webhooks():
    if request.method =='POST':
        repo = git.Repo('/home/getyourmusic/get_your_music')
        origin = repo.remotes.origin
        origin.pull()
        return 'Updated PythonAnywhere successfully', 200
    else:
        return 'SOMETHING WENT WRONG', 400

 
if __name__ == '__main__': 
    app.run(debug=True,host="0.0.0.0")
