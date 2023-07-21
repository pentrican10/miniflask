from flask import Flask, render_template, request, session, redirect, url_for
import plotly.express as px
from astropy.io import fits
import pandas as pd
import os

#currently the star_id triggers a dynamic url,
#but the project_dir is on its own url "/submit_project_dir"


app = Flask(__name__)
app.secret_key='secret'

@app.route('/', methods=['GET', 'POST'])
def star_input():
    star_id = None
    project_dir = None

    if request.method == 'POST':
        project_dir = request.form['project_dir']
        session['project_dir']=project_dir
    elif request.method == 'GET':
        star_id = request.args.get('star_id')
        session['star_id']=star_id
        if star_id:
            return redirect(url_for('process_star', star_id=star_id, project_dir=project_dir))

    return render_template('index1.html', star_id=star_id, project_dir=project_dir)

@app.route('/<star_id>')
def process_star(star_id):
    project_dir=session.get('project_dir')
    # Here you can process the star_id as per your requirement
    return render_template('index1.html', star_id=star_id, project_dir=project_dir)

@app.route('/submit_project_dir', methods=['POST'])
def submit_project_dir():
    star_id = session.get('star_id')
    project_dir = request.form['project_dir']
    return render_template('index1.html', project_dir=project_dir, star_id=star_id)

if __name__ == '__main__':
    app.run(debug=True)
