from flask import Flask, render_template, request, session, redirect, url_for
import plotly.express as px
from astropy.io import fits
import pandas as pd
import os

app = Flask(__name__)
app.secret_key='secret'

@app.route('/')
def index():
    #clear all sesison variables on boot up
    session['project_dir']=None
    session['star_id']=None
    session['data_dir']=None
    return redirect(url_for('home'))

@app.route('/home')
def home():
    return render_template('index.html', 
                           project_dir=None, 
                           star_id=None, 
                           plot_div=None,
                           no_data=None
                          )


@app.route('/save_project_dir', methods=['POST'])
def save_project_dir():
    project_dir= request.form.get('project_dir') 
    session['project_dir']=project_dir
    data_dir=os.path.join(project_dir, 'miniflask', 'kepler_lightcurves_for_paige')
    session['data_dir']=data_dir
    return render_template('index.html', 
                           project_dir=project_dir, 
                           star_id=session.get('star_id') 
                          )

@app.route('/save_star_id', methods=['POST'])
def save_star_id():
    star_id = request.form.get('star_id')
    session['star_id']=star_id 
    return render_template('index.html', 
                           project_dir=session.get('project_dir'),
                           star_id=star_id
                          )

@app.route('/plot', methods=['POST'])
def plot():
    project_dir=session.get('project_dir')
    data_dir=session.get('data_dir')
    star_id=session.get('star_id')
    file_name = star_id +'_lc_detrended.fits'
    file_path = os.path.join(data_dir, file_name)

    #get data and create figure
    if os.path.isfile(file_path):
        data = read_data_from_fits(file_path)
        fig = px.scatter(data, x="TIME", y="FLUX", 
                    title="Kepler Detrended Light Curve")
        plot_div = fig.to_html(full_html=False, include_plotlyjs='cdn')
        return render_template('index.html',  
                            project_dir=project_dir, 
                            star_id =star_id,
                            plot_div=plot_div
                           )
    else:
        no_data = f'No data found for { star_id } in directory { project_dir }'
        return render_template('index.html', 
                           project_dir=project_dir, 
                           star_id =star_id,
                           no_data=no_data
                          )


def read_data_from_fits(file_path):
    fits_file = fits.open(file_path)
    time = fits_file[1].data
    flux = fits_file[2].data
    df = pd.DataFrame(dict(
        TIME=time,
        FLUX=flux
    ))
    return df


if __name__ == '__main__':
    app.run(debug=True)
