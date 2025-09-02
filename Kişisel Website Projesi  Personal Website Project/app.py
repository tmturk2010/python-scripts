from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit():
    name = request.form.get("name")
    is_checked = "isChecked" in request.form
    with open("data.txt", "a") as f:
        f.write(f"Name {name}, Checked? {is_checked}\n")
       # return f"Name: {name}, Checkbox checked? {is_checked}"
    # eğer inputu ekrana yazdırcaksan line 17'yi comment'le 15'i uncomment'le
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")