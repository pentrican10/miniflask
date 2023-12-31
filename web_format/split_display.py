from flask import Flask, render_template, jsonify, request
import os
import csv
import plotly.express as px
from astropy.io import fits
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
#split display demo

#comments box show up on load
# comments.txt master file for comments
# comments will be entered:
    #datetime
    #user
        #comment
    # /n

#display current star, if no star, then pop up saying star must be selected


app = Flask(__name__)

@app.route('/')

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
    comment = request.form.get('comment')
    action = request.form.get('action')
    #if comment and action in ['overwrite','append']:
    with open(file_path, 'w' if action == 'overwrite' else 'a') as file:
        file.write("\n")
        #file.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        #file.write(f"User: {current_user}\n")
        file.write(f"Comment: {comment}\n")
            
        # button to maually edit file and pull up file
        # pop up txt file and edit text, new window, warn directly editing comments file

    return display_comment_file(koi_id)
    

if __name__ == '__main__':
    app.run(debug=True)



"""
@app.route('/star/<koi_id>/plot')
def generate_plot(koi_id):
    star_id = koi_id.replace("K","S")
    file_name = star_id + '_lc_detrended.fits'
    file_path = os.path.join('C:\\Users\\Paige\\Projects','miniflask','kepler_lightcurves_for_paige',file_name)

    #get data and create figure
    if os.path.isfile(file_path):
        data = read_data_from_fits(file_path)
        fig = px.scatter(data, x="TIME", y="FLUX", 
                    title="Kepler Detrended Light Curve")
        plot_div = fig.to_html(full_html=False, include_plotlyjs='cdn')
        #return plot_div
    else:
        plot_div = f'No data found for { koi_id } in directory'
    return plot_div
    

def read_data_from_fits(file_path):
    fits_file = fits.open(file_path)
    time = fits_file[1].data
    flux = fits_file[2].data
    df = pd.DataFrame(dict(
        TIME=time,
        FLUX=flux
    ))
    return df
"""