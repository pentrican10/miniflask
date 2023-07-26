from flask import Flask, render_template
import os
import csv

#split display demo

app = Flask(__name__)

@app.route('/')

def display_table_data():
    table_data = read_table_data()
    left_content = render_template('left.html', table_data=table_data)
    right_content = render_template('right.html')
    return render_template('index1.html',left_content=left_content, right_content=right_content)

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
