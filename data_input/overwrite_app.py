from flask import Flask, render_template, request

# this app will take user input, overwrite txt file, and display

app=Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/save', methods=['POST'])
def save():
    input_text = request.form['inputField']
    action = request.form['actionButton']
    #overwrite = request.form['overwriteButton'] == 'true'
    #save to txt file
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