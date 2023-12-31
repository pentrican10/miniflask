from flask import Flask, render_template, request

app = Flask(__name__)

def read_file_contents():
    try:
        with open('myfile.txt', 'r') as file:
            return file.read()
    except Exception as e:
        return ""

@app.route('/')
def index():
    current_contents = read_file_contents()
    return render_template('index.html', current_contents=current_contents, updated_contents="")

@app.route('/update', methods=['POST'])
def update_file():
    new_contents = request.form.get('file_contents')
    try:
        with open('myfile.txt', 'w') as file:
            file.write(new_contents)
        updated_contents = new_contents  # Use the new contents as updated contents
        return render_template('index.html', current_contents=new_contents, updated_contents=updated_contents)
    except Exception as e:
        return f"An error occurred: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)





"""
from flask import Flask, render_template 
import csv
import os

app = Flask(__name__)

#display table on web app

@app.route('/')
def display_table_data():
    table_data = read_table_data()
    return render_template('index.html',table_data=table_data)

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


if __name__ == '__main__':
    app.run(debug=True)

"""