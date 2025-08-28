from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit():
    name = request.form.get("name")
    is_checked = "isChecked" in request.form
    # buraya bişi ekleyebilirim
    return f"Name: {name}, Checkbox checked? {is_checked}"

if __name__ == "__main__":
    app.run(debug=True)