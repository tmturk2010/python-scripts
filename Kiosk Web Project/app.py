from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")
    
@app.route("/submit", methods=["POST"])
def submit():
    name = request.form.get("name")
    with open("data.txt", "a") as f:
        f.write(f"Name {name}\n")
        return f"Name: {name}"

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")