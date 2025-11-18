from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# --------------------------
# 1. MySQL database configuration (edit based on your environment)
# --------------------------
# Format: mysql+pymysql://username:password@host/database?params
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:password@localhost/top5db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# --------------------------
# 2. Database Model Definition
# --------------------------
class Submission(db.Model):
    __tablename__ = "submissions"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category = db.Column(db.String(255), nullable=False)
    item1 = db.Column(db.String(255), nullable=False)
    item2 = db.Column(db.String(255), nullable=False)
    item3 = db.Column(db.String(255), nullable=False)
    item4 = db.Column(db.String(255), nullable=False)
    item5 = db.Column(db.String(255), nullable=False)

    @property
    def five(self):
        """Return the five items as a list (keeps compatibility with template)."""
        return [self.item1, self.item2, self.item3, self.item4, self.item5]


# --------------------------
# 3. Route Logic
# --------------------------
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        # Get the category and the top five items from the form
        category = request.form.get("category", "").strip()
        items = [request.form.get(f"item{i}", "").strip() for i in range(1, 6)]

        # Validate that all fields are filled
        if category and all(items):
            submission = Submission(
                category=category,
                item1=items[0],
                item2=items[1],
                item3=items[2],
                item4=items[3],
                item5=items[4],
            )
            db.session.add(submission)
            db.session.commit()

        return redirect("/")

    # Fetch all submissions from the database
    submissions = Submission.query.order_by(Submission.id.asc()).all()
    return render_template("index.html", submissions=submissions)


if __name__ == "__main__":
    # Create the database tables on first run
    with app.app_context():
        db.create_all()
    app.run(debug=True)
