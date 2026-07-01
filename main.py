from flask import Flask ,render_template ,url_for ,request ,redirect ,session ,flash
from models import db, User ,Prediction
from werkzeug.security import check_password_hash
import os
from werkzeug.utils import secure_filename
from ai.predict_utils import predict_image
from disease_info import DISEASE_INFO

app = Flask(__name__)
UPLOAD_FOLDER = "static/uploads"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
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

    # Get uploaded image
    image = request.files.get("image")

    if image is None:
        flash("No image uploaded.", "danger")
        return redirect(url_for("detect"))

    if image.filename == "":
        flash("Please select an image first.", "warning")
        return redirect(url_for("detect"))

    # Safe filename
    filename = secure_filename(image.filename)

    # Save image
    image_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        filename
    )

    image.save(image_path)

    # AI Prediction
    disease, confidence = predict_image(image_path)
    info = DISEASE_INFO.get(
    disease,
    {
        "medicine": "Not Available",
        "treatment": "No recommendation available.",
        "prevention": "Consult an agricultural expert."
    }
)
    crop = disease.split("___")[0]

    prediction = Prediction(
    user_id=session["user_id"],
    image=image_path,
    crop_name=crop,
    disease=disease,
    confidence=round(confidence,2))
    db.session.add(prediction)
    db.session.commit()

    return render_template(
    "result.html",
    image=image_path,
    disease=disease,
    confidence=round(confidence, 2),
    medicine=info["medicine"],
    treatment=info["treatment"],
    prevention=info["prevention"]
)
@app.route("/view_prediction/<int:id>")
def view_prediction(id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    prediction = Prediction.query.get_or_404(id)

    if prediction.user_id != session["user_id"]:
        flash("Unauthorized access.", "danger")
        return redirect(url_for("history"))

    return render_template(
        "result.html",
        image=prediction.image,
        disease=prediction.disease,
        confidence=prediction.confidence
    )

@app.route("/delete_prediction/<int:id>")
def delete_prediction(id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    prediction = Prediction.query.get_or_404(id)

    if prediction.user_id != session["user_id"]:
        flash("Unauthorized access.", "danger")
        return redirect(url_for("history"))

    db.session.delete(prediction)
    db.session.commit()

    flash("Prediction deleted successfully.", "success")

    return redirect(url_for("history"))

@app.route("/history")
def history():

    predictions = Prediction.query.filter_by(
        user_id=session["user_id"]
    ).order_by(
        Prediction.created_at.desc()
    ).all()

    return render_template(
        "history.html",
        predictions=predictions
    )


@app.route("/profile")
def profile():

    if "user_id" not in session:
        return redirect(url_for("login"))

    user = User.query.get(session["user_id"])

    total_scans = Prediction.query.filter_by(
        user_id=user.id
    ).count()

    disease_count = Prediction.query.filter(
        Prediction.user_id == user.id,
        Prediction.disease.notlike("%healthy%")
    ).count()

    return render_template(
        "profile.html",
        user=user,
        total_scans=total_scans,
        disease_count=disease_count
    )


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
