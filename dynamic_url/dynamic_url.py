
from flask import Flask, render_template, request, session, jsonify, redirect, url_for

app = Flask(__name__)

@app.route('/')
def star_input():
    return render_template('index.html')

@app.route('/<star_id>')
def process_star(star_id):
    return render_template('index.html', star_id=star_id)


if __name__ == '__main__':
    app.run(debug=True)