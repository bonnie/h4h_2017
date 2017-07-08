from flask import Flask, render_template, request
from food_shelters import find_nearest_resource

app = Flask(__name__)

@app.route("/")
def show_homepage():
    return render_template('index.html')

@app.route("/shelter")
def show_nearest_shelter():
    current_address = request.args.get('address')
    nearest = find_nearest_resource(current_address)
    return render_template("results.html", shelter=nearest)

if __name__ == "__main__":
    app.run(debug=True)