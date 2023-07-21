from flask import Flask, render_template, request, session, redirect, url_for
import plotly.express as px
from astropy.io import fits
import pandas as pd
import os

#test assignment read and plot, do it through a web app, enter dir and ID and display plot

#pass all variables to render_template

app = Flask(__name__)
app.secret_key='secret'


@app.route('/', methods=['GET', 'POST'])
def index(): #make index only called when first boot up app
    plot_div=None 
    star_id=None
    project_dir=None
    data_dir=None

    if request.method == 'POST':
        project_dir = request.form.get('project_dir')   #this could be why the proj dir disappears, requests the dir every time the button is pressed
        session['project_dir']=project_dir
        data_dir=session.get('data_dir')

        star_id=session.get('star_id')
        file_name = star_id +'_lc_detrended.fits'
        file_path = os.path.join(data_dir, file_name)

        #get data and create figure
        data = read_data_from_fits(file_path)
        fig = px.scatter(data, x="TIME", y="FLUX", 
                 title="Kepler Detrended Light Curve")
        plot_div = fig.to_html(full_html=False, include_plotlyjs='cdn')

        return render_template('index.html', plot_div=plot_div, project_dir=project_dir, star_id =star_id)

    project_dir = session.get('project_dir') #None
    if project_dir:
        data_dir = os.path.join(project_dir, 'kepler_lightcurves_for_paige')
        session['data_dir']= data_dir

    data_dir=session.get('data_dir')
    return render_template('index.html', plot_div=plot_div,star_id =star_id, project_dir=project_dir) #, data_dir=data_dir)


@app.route('/save_project_dir', methods=['POST'])
def save_project_dir():
    project_dir= request.form.get('project_dir')  #changed this to get and THEN set as session variable
    session['project_dir']=project_dir
    #return redirect(url_for('index'))
    return render_template('index.html')

@app.route('/save_star_id', methods=['POST'])
def save_star_id():
    star_id = request.form.get('star_id')
    session['star_id']=star_id 
    project_dir = session.get('project_dir','')
    #star_file_content = read_star_file(star_id)
    data_dir = session.get('data_dir') #None
    return render_template('index.html', star_id=star_id, project_dir=project_dir)

def read_data_from_fits(file_path): #eventually want to make it to it is based on user input
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

