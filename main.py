from flask import Flask ,render_template ,url_for ,request ,redirect ,session ,flash
from models import db, User ,Prediction
from werkzeug.security import check_password_hash

app = Flask(__name__)
app.secret_key = "farmerscam_secret_key"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

@app.route("/")
def home():
    return redirect(url_for("login"))

@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect(url_for("login"))

    return render_template("index.html")

@app.route("/detect")
def detect():

    if "user_id" not in session:
        return redirect(url_for("login"))

    return render_template("detection.html")

@app.route("/predict", methods=["POST"])
def predict():

    image = request.files["image"]

    # Temporary prediction
    disease = "Tomato Late Blight"

    return f"Prediction: {disease}"


@app.route("/history")
def history():

    if "user_id" not in session:
        return redirect(url_for("login"))

    return render_template("history.html")


@app.route("/profile")
def profile():

    if "user_id" not in session:
        return redirect(url_for("login"))

    user = User.query.get(session["user_id"])

    return render_template("profile.html",user=user)


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()

        if user is None:
            flash("Email not registered.", "danger")
            return redirect(url_for("login"))

        # Since you're currently storing plain text passwords
        if user.password == password:
            session["user_id"] = user.id
            session["user_name"] = user.name

            flash(f"Welcome {user.name}!", "success")
            return redirect(url_for("dashboard"))

        flash("Incorrect Password.", "danger")
        return redirect(url_for("login"))

    return render_template("login.html")



@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        if password != confirm_password:
            flash("Passwords do not match!", "danger")
            return redirect(url_for("register"))

        # Check existing email
        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            flash("Email already exists.", "warning")
            return redirect(url_for("register"))

        user = User(
            name=name,
            email=email,
            phone=phone,
            password=password
        )

        db.session.add(user)
        db.session.commit()

        flash("Registration Successful! Please Login.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully.", "info")
    return redirect(url_for("login"))

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
