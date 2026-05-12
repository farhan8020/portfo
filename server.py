from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message

app = Flask(__name__)

# =========================
# DATABASE CONFIGURATION
# =========================

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gym.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# =========================
# EMAIL CONFIGURATION
# =========================

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True

# YOUR GMAIL
app.config['MAIL_USERNAME'] = 'thedengym0@gmail.com'

# GOOGLE APP PASSWORD
app.config['MAIL_PASSWORD'] = 'cycmrcuaosuwtgta'

mail = Mail(app)

# =========================
# DATABASE MODEL
# =========================

class Contact(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    fullname = db.Column(db.String(100))

    phone = db.Column(db.String(20))

    message = db.Column(db.Text)

# =========================
# CREATE DATABASE
# =========================

with app.app_context():
    db.create_all()

# =========================
# ROUTES
# =========================

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about-us.html")

@app.route("/services")
def services():
    return render_template("services.html")

@app.route("/team")
def team():
    return render_template("team.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/thankyou")
def thankyou():
    return render_template("thankyou.html")

# =========================
# ADMIN PANEL
# =========================

@app.route("/admin")
def admin():

    enquiries = Contact.query.all()

    return render_template(
        "admin.html",
        enquiries=enquiries
    )

# =========================
# CONTACT FORM SUBMIT
# =========================

@app.route("/submit_form", methods=["POST"])
def submit_form():

    fullname = request.form.get("fullname")
    phone = request.form.get("phone")
    message = request.form.get("message")

    # SAVE TO DATABASE

    new_contact = Contact(
        fullname=fullname,
        phone=phone,
        message=message
    )

    db.session.add(new_contact)
    db.session.commit()

    print("FORM SUBMITTED")

    # SEND EMAIL

    msg = Message(
        subject="New Gym Enquiry",
        sender=app.config['MAIL_USERNAME'],
        recipients=["thedengym0@gmail.com"]
    )

    msg.body = f"""
New Gym Enquiry

Name: {fullname}

Phone: {phone}

Message:
{message}
"""

    mail.send(msg)

    print("EMAIL SENT")

    return redirect("/thankyou")

# =========================
# RUN SERVER
# =========================

if __name__ == "__main__":
    app.run(debug=True)
