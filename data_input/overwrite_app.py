from flask import Flask, render_template, request, redirect, url_for
import os
# this app will take user input, overwrite txt file, and display

# note: make it so it can't save empty lines to the txt file
#       make it so it doesn't go to new route (like '/save')
#       box doesnt resize

app=Flask(__name__)

@app.route('/')
def index():
    return redirect(url_for('home'))

@app.route('/home')
def home():
    return render_template('index.html')

"""
@app.route('/starid', methods=['GET'])
def starid():
    star_id = request.form['star_id']
    file_path= os.path.join(app.root_path, star_id)
    #read content
    #file_content = ''
    if os.path.isfile(file_path):
        file_content='File found!'
        #with open(file_path, 'r') as file:
        #    file_conent = file.read()
    else:
        file_content = 'File not found!'
    return render_template('index.html', file_content=file_content)
"""
@app.route('/home', methods=['POST'])
def save():
    #file_path = 
    input_text = request.form['inputField']
    action = request.form['actionButton']
    #save to txt file
    if input_text == '':
        return display()
    else:
        if action == 'overwrite':
            #overwrite txt
            with open('input.txt', 'w') as file:
                file.write(input_text+'\n')
        elif action == 'append':
            #append file
            with open('input.txt', 'a') as file:    # 'w' would overwrite the doccument
                file.write(input_text+'\n')
    return display()

@app.route('/display')
def display():
    #read txt file
    with open('input.txt', 'r') as file:
        file_content = file.readlines()
    return render_template('index.html', file_content=file_content)

if __name__ == '__main__':
    app.run()