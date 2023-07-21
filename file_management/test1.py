from flask import Flask, render_template, request, redirect, url_for, session
import os

# os.path.expanduser('~')

#save directory as session variable, tracking it

app=Flask(__name__)
app.secret_key = 'secret'

@app.route('/')
def index():
    return redirect(url_for('home'))

@app.route('/home')
def home():
    return render_template('index1.html')

@app.route('/directory', methods=['POST'])
def project_directory():
    project_dir = request.form['project_dir']
    data_dir = os.path.join(project_dir, 'miniflask','file_management','comments')
    session['data_dir']= data_dir
    return redirect(url_for('home'))


@app.route('/starid', methods=['POST'])
def display_file():
    star_id = request.form['star_id']
    file_content = read_text_file(star_id)
    return render_template('index1.html', file_content=file_content)

def read_text_file(star_id):
    #base_path = data_dir
    data_dir = session['data_dir']

    file_name = star_id + '_comments.txt'
    file_path= os.path.join(data_dir, star_id, file_name)
    #read content
    if not os.path.isfile(file_path):
        return 'File not found.'


    with open(file_path, 'r') as file:
        file_content = file.readlines()
    return file_content



if __name__ == '__main__':
    app.run(debug=True)
