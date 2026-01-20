from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['UPLOAD_FOLDER'] = 'static/uploads'

db = SQLAlchemy(app)

class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    issue_type = db.Column(db.String(100))
    description = db.Column(db.String(300))
    status = db.Column(db.String(20), default="Active")
    image = db.Column(db.String(200))

@app.route("/")
def report():
    return render_template("report.html")

@app.route("/submit", methods=["POST"])
def submit():
    image = request.files["image"]
    filename = image.filename
    image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    report = Report(
        issue_type=request.form["issue"],
        description=request.form["description"],
        image=filename
    )
    db.session.add(report)
    db.session.commit()
    return redirect(url_for("dashboard"))

@app.route("/dashboard")
def dashboard():
    total = Report.query.count()
    active = Report.query.filter_by(status="Active").count()
    resolved = Report.query.filter_by(status="Resolved").count()
    reports = Report.query.all()

    return render_template(
        "dashboard.html",
        total=total,
        active=active,
        resolved=resolved,
        reports=reports
    )

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
