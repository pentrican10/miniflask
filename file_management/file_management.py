from flask import Flask, render_template, request, session, redirect, url_for
import os
app = Flask(__name__)
app.secret_key='secret'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        session['project_dir'] = request.form.get('project_dir') #None
        #session['project_dir']=project_dir

    project_dir = session.get('project_dir') #None
    data_dir = os.path.join(project_dir, 'miniflask','file_management','comments')
    session['data_dir']= data_dir
    return render_template('index.html', project_dir=project_dir, data_dir=data_dir)

@app.route('/save_project_dir', methods=['POST'])
def save_project_dir():
    session['project_dir']= request.form.get('project_dir') #None
    return redirect(url_for('index'))

def read_star_file(star_id):
    data_dir = session['data_dir']
    file_name = star_id + '_comments.txt'
    file_path = os.path.join(data_dir, star_id, file_name)
    if not os.path.isfile(file_path):
        return 'File not found.'

    with open(file_path, 'r') as file:
        file_content = file.read()
    return file_content

@app.route('/save_star_id', methods=['POST'])
def save_star_id():
    star_id = request.form.get('star_id')
    star_file_content = read_star_file(star_id)
    data_dir = session.get('data_dir') #None
    return render_template('index.html', data_dir=data_dir, star_id=star_id, star_file_content=star_file_content)

if __name__ == '__main__':
    app.run(debug=True)
