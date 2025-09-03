from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")
    
@app.route("/product")
def product():
    return render_template("product.html")

@app.route("/cart")
def cart():
    return render_template("cart.html")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")