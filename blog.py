from flask import Flask , render_template,flash,redirect,url_for,session,logging,request
from flask_mysqldb import MySQL
from wtforms import Form,StringField,TextAreaField,PasswordField,validators
from passlib.hash import sha256_crypt
from functools import wraps

#Kullacını Giriş Decorator'ı
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "logged_in" in session:
            return f(*args, **kwargs)
        else:
            flash("Please login to the website!" , "danger")
            return redirect(url_for("login"))       
    return decorated_function

#Kullanıcı Kayıt Formu
class RegisterForm(Form):
    name = StringField("Name Surname: " , validators=[validators.Length(min=4,max=25)])
    username = StringField("Username: " , validators=[validators.Length(min=6,max=20)])
    email = StringField("Email Address: " , validators=[validators.Email(message = "Please add a real email address")])
    password = PasswordField("Password: " , validators=[
        validators.DataRequired(message="Please write a password"),
        validators.EqualTo(fieldname= "confirm" , message="Passwords not matched!")
    ])
    confirm = PasswordField("Password confirmation")
class LoginForm(Form):
    username = StringField("Username")
    password = PasswordField("Password")

app = Flask(__name__)
app.secret_key = "msblog"
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "msblog"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)

@app.route("/")
def index():
    return render_template("index.html")
@app.route("/about")
def about():
    return render_template("about.html")

#Gezi sayfası
@app.route("/journeys")
def journeys():
    cursor = mysql.connection.cursor()
    sorgu = "Select * From journeys"
    result = cursor.execute(sorgu)

    if result > 0:
        journeys = cursor.fetchall()
        return render_template("journeys.html", journeys = journeys)
    else:
        return render_template("journeys.html")

@app.route("/dashboard")
@login_required
def dashboard():
    cursor = mysql.connection.cursor()
    sorgu = "Select * from journeys where author = %s"
    result = cursor.execute(sorgu, (session["username"],))

    if result > 0:
        journeys = cursor.fetchall()
        return render_template("dashboard.html", journeys = journeys)
    else:
        return render_template("dashboard.html")



@app.route("/register" , methods = ["GET" , "POST"])
def register():
    form = RegisterForm(request.form)

    if request.method == "POST" and form.validate():
        name = form.name.data
        username = form.username.data
        email = form.email.data
        password = sha256_crypt.encrypt(form.password.data)

        cursor = mysql.connection.cursor()

        sorgu = "Insert into users(name,email,username,password) VALUES(%s,%s,%s,%s)"

        cursor.execute(sorgu,(name,email,username,password))
        mysql.connection.commit()

        cursor.close()
        flash("Sign Up Successful!","success")

        return redirect(url_for("login"))
    else:
        return render_template("register.html" , form = form)

#Login işlemi
@app.route("/login", methods =["GET","POST"])
def login():
    form = LoginForm(request.form)
    if request.method == "POST":
        username = form.username.data
        password_entered = form.password.data
        cursor = mysql.connection.cursor()
        sorgu = "Select * From users where username = %s"
        result = cursor.execute(sorgu,(username,))
        if result >0:
            data = cursor.fetchone()
            real_password = data["password"]
            if sha256_crypt.verify(password_entered,real_password):
                flash("Login successful..." , "success")
                session["logged_in"] = True
                session["username"] = username
                return redirect(url_for("index"))
            else:
                flash("Sorry, your password was wrong. Please check your password carefully." , "danger")
                return redirect(url_for("login"))
        else:
            flash("This username is not used...", "danger")
            return redirect(url_for("login"))
    return render_template("login.html", form = form)

#Detay Sayfası
@app.route("/journey/<string:id>")
def journey(id):
    cursor = mysql.connection.cursor()
    sorgu = "Select * From journeys where id = %s"
    result = cursor.execute(sorgu,(id,))

    if result > 0:
        journey = cursor.fetchone()
        return render_template("journey.html", journey = journey)
    else:
        return render_template("journey.html")

#Sign Out İşlemi
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


#Gezi ekleme
@app.route("/addjourney" , methods = ["GET","POST"])
@login_required
def addjourney():
    form = ArticleForm(request.form)
    if request.method == "POST" and form.validate():
        title = form.title.data
        content = form.content.data
        cursor = mysql.connection.cursor()
        sorgu = "Insert into journeys(title,author,content) VALUES(%s,%s,%s)"
        cursor.execute(sorgu,(title,session["username"],content))
        mysql.connection.commit()
        cursor.close()
        flash("Travel added successfully","success" )
        return redirect(url_for("dashboard"))
    return render_template("addjourney.html", form = form)

#Gezi Silme İşlemi
@app.route("/delete/<string:id>")
@login_required
def delete(id):
    cursor = mysql.connection.cursor()
    sorgu = "Select * from journeys where author = %s and id = %s"
    result =cursor.execute(sorgu,(session["username"],id))

    if result > 0:
        sorgu2 = "Delete from journeys where id = %s"
        cursor.execute(sorgu2,(id,))
        mysql.connection.commit()
        return redirect(url_for("dashboard"))
    else:
        flash("There is no such trip or you are not authorized to delete this trip!","danger")
        return redirect(url_for("index"))
        
#Gezi Güncelleme İşlemi
@app.route("/edit/<string:id>",methods = ["GET","POST"])
@login_required
def update(id):    
    if request.method == "GET":
        cursor = mysql.connection.cursor()
        sorgu = "Select * from journeys where id = %s and author = %s"
        result =cursor.execute(sorgu,(session["username"],id))

        if result == 0:
            flash("There is no such trip or you are not authorized to delete this trip!","danger")
            return redirect(url_for("index"))
        else:
            journey = cursor.fetchone()
            form = ArticleForm()

            form.title.data = journey["title"]
            form.content.data = journey["content"]
            return render_template("update.html", form = form)

    else:
        #POST REQUEST KISMI
        form = ArticleForm(request.form)
        newTitle = form.title.data
        newContent = form.content.data

        sorgu2 = "update journeys Set title = %s, content = %s where id = %s"
        cursor = mysql.connection.cursor()
        cursor.execute(sorgu2,(newTitle,newContent,id))
        mysql.connection.commit()
        flash("The trip was successfully updated", "success")
        return redirect(url_for("dashboard"))


#Gezi Form
class ArticleForm(Form):
    title = StringField("Travel Title" , validators=[validators.Length(min=3 , max=100)])
    content = TextAreaField("About Travel", validators=[validators.Length(min = 10)]) 

#Arama URL
@app.route("/search", methods = ["GET","POST"])
def search():
    if request.method == "GET":
        return redirect(url_for("index"))
    else:
        keyword = request.form.get("keyword")
        cursor = mysql.connection.cursor()
        sorgu = "Select * from journeys where title like '%"+ keyword +"%' "
        result = cursor.execute(sorgu)

        if result == 0:
            flash("No trip found for your search ", "warning")
            return redirect(url_for("journeys"))
        else:
            journeys = cursor.fetchall()
            return render_template("journeys.html", journeys = journeys) 

if __name__ == "__main__":
    app.run(debug=True)