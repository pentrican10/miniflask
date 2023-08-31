from flask import Flask, render_template, jsonify, request, session, redirect, url_for
import os
import csv
from datetime import datetime
import plotly.express as px
from astropy.io import fits
import pandas as pd
import json
import plotly.utils
import plotly.graph_objects as go
from plotly.subplots import make_subplots



app = Flask(__name__)
app.secret_key = 'super_secret'

@app.route('/')
def index():
    session.clear()
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        if username:
            session['username'] = username
            return redirect(url_for('display_table_data'))
    return render_template('login.html')

@app.route('/logout',methods=['POST'])
def logout():
    session.pop('username',None) #removes username
    return redirect(url_for('login'))

@app.route('/home')
def display_table_data():
    table_data = read_table_data()
    left_content = render_template('left.html', table_data=table_data)
    right_top_content = render_template('right_top.html')
    right_bottom_content = render_template('right_bottom.html')
    return render_template('index1.html',left_content=left_content, right_top_content=right_top_content, right_bottom_content=right_bottom_content)



def read_table_data():
    file_path = os.path.join(os.path.dirname(__file__), 'data', '2023-05-19_singles.csv')
    table_data = []
    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            #round table values
            row['kep_mag'] = round(float(row['kep_mag']), 2)
            row['Rstar'] = round(float(row['Rstar']), 2)
            row['logrho'] = round(float(row['logrho']), 2)
            row['Teff'] = round(float(row['Teff']))
            row['logg'] = round(float(row['logg']), 2)
            table_data.append(row)
    return table_data


@app.route('/star/<koi_id>')
def display_comment_file(koi_id):
    file_path = os.path.join('C:\\Users\\Paige\\Projects','miniflask','comment_files',f'{koi_id}_comments.txt')
    if os.path.isfile(file_path):
        with open(file_path, 'r') as file:
                file_content = file.read()
    else:
        file_content = f'Comment file for {koi_id} not found.'
    return file_content

@app.route('/star/<koi_id>/save_comment', methods=['POST'])
def save_comment(koi_id):
    file_path = os.path.join('C:\\Users\\Paige\\Projects','miniflask','comment_files',f'{koi_id}_comments.txt')
    comment = request.form.get('comment').strip()
    username = session.get('username')
    with open(file_path, 'a') as file:
        file.write("\n")
        file.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        file.write(f"User: {username}\n")
        file.write(f"Comment: {comment}\n")
    return display_comment_file(koi_id)

@app.route('/star/<koi_id>/edit_file', methods=['POST'])
def save_file(koi_id):
    file_path = os.path.join('C:\\Users\\Paige\\Projects', 'miniflask', 'comment_files', f'{koi_id}_comments.txt')
    content = request.form.get('content')
    # Normalize line endings to Unix-style (\n)
    content = content.replace('\r\n', '\n')
    try:
        with open(file_path, 'w') as file:
            file.writelines(content)
            file.write('\n')
        return display_comment_file(koi_id)
    except Exception as e:
        return f"An error occurred: {str(e)}"

@app.route('/generate_plot/<koi_id>')
def generate_plot(koi_id):
    star_id = koi_id.replace("K","S")
    file_name = star_id + '_lc_detrended.fits'
    file_path = os.path.join('C:\\Users\\Paige\\Projects','miniflask','kepler_lightcurves_for_paige',file_name)
    #get data and create detrended light curve
    if os.path.isfile(file_path):
        data = read_data_from_fits(file_path)
        fig = px.scatter(data, x="TIME", y="FLUX", 
                    title="Kepler Detrended Light Curve")
        graph1JSON= json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder) #possibly check if cls defined to differentiate 
        return jsonify(graph1JSON)
    else:
        error_message = f'No data found for {koi_id}'
        return jsonify(error_message=error_message)
        

def read_data_from_fits(file_path):
    with fits.open(file_path) as fits_file:
        time = fits_file[1].data
        flux = fits_file[2].data
        df = pd.DataFrame(dict(
            TIME=time,
            FLUX=flux
        ))
    return df

if __name__ == '__main__':
    app.run(debug=True)

