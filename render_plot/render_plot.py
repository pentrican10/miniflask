from flask import Flask, render_template, request, session, redirect, url_for
import plotly.graph_objs as go
import plotly.express as px
from astropy.io import fits
import pandas as pd
import os

#test assignment read and plot, do it through a web app, enter dir and ID and display plot

app = Flask(__name__)
app.secret_key='secret'

#############################################################################################################################
@app.route('/', methods=['GET', 'POST'])
def index():
    plot_div=None #what is this
    
    if request.method == 'POST':
        project_dir = request.form.get('project_dir')
        session['project_dir']=project_dir
        #session['project_dir'] = request.form.get('project_dir', '') #None
        #session['project_dir']=project_dir
        data_dir=session.get('data_dir')
        #star_id = request.form.get('star_id')
        star_id=session.get('star_id')
        file_name = star_id +'_lc_detrended.fits'
        file_path = os.path.join(data_dir, file_name)
        data = read_data_from_fits(file_path)

        fig = px.scatter(data, x="TIME", y="FLUX", 
                 title="Kepler Detrended Light Curve")
        
        plot_div = fig.to_html(full_html=False, include_plotlyjs='cdn')

        return render_template('index.html', plot_div=plot_div, project_dir=project_dir)

    project_dir = session.get('project_dir') #None
    if project_dir:
        data_dir = os.path.join(project_dir, 'kepler_lightcurves_for_paige')
        session['data_dir']= data_dir

    data_dir=session.get('data_dir')
    return render_template('index.html', project_dir=project_dir, data_dir=data_dir)


@app.route('/save_project_dir', methods=['POST'])
def save_project_dir():
    session['project_dir']= request.form.get('project_dir') #None
    return redirect(url_for('index'))

@app.route('/save_star_id', methods=['POST'])
def save_star_id():
    star_id = request.form.get('star_id')
    session['star_id']=star_id ##################
    project_dir = session.get('project_dir','')
    #star_file_content = read_star_file(star_id)
    data_dir = session.get('data_dir') #None
    return render_template('index.html', data_dir=data_dir, star_id=star_id)


##############################################################################################################################


#path=Path("C:\Users\Paige\Projects\kepler_lightcurves_for_paige\S00600_lc_detrended.fits")
def read_data_from_fits(file_path): #eventually want to make it to it is based on user input
    fits_file = fits.open(file_path)
    time = fits_file[1].data
    flux = fits_file[2].data
    df = pd.DataFrame(dict(
        TIME=time,
        FLUX=flux
    ))
    return df

"""
@app.route('/',methods=['GET','POST'])
def plot_data():
    plot_div=None #what is this

    if request.method == 'POST':
        data_dir=session.get('data_dir')
        #star_id = request.form.get('star_id')
        star_id=session.get('star_id')
        file_name = star_id +'_lc_detrended.fits'
        file_path = os.path.join(data_dir, 'kepler_lightcurves_for_paige', file_name)
        data = read_data_from_fits(file_path)

        fig = px.scatter(data, x="TIME", y="FLUX", 
                 title="Kepler Detrended Light Curve S00600")
        
        plot_div = fig.to_html(full_html=False, include_plotlyjs='cdn')

    return render_template('index.html', plot_div=plot_div)
       """ 



if __name__ == '__main__':
    app.run(debug=True)

