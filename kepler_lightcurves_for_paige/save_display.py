from flask import Flask, render_template, request

# this app will take user input, save to txt file, and display all entries in the txt file

app=Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/save', methods=['POST'])
def save():
    input_text = request.form['inputField']
    #save to txt file
    with open('input.txt', 'a') as file:    # 'w' would overwrite the doccument
        file.write(input_text+'\n')

    return display()

@app.route('/display')
def display():
    #read txt file
    with open('input.txt', 'r') as file:
        file_content = file.readlines()
    return render_template('display.html', file_content=file_content)

if __name__ == '__main__':
    app.run()