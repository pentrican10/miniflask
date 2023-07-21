from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/display', methods=['POST'])
def display():
    input_text = request.form['inputField']
    return render_template('display.html', input_text=input_text)

@app.route('/save', methods=['POST'])
def save():
    input_text = request.form['inputField']
    #save input_text to text file
    with open('input.txt', 'a') as file:
        file.write(input_text)
    return render_template('success.html')

if __name__ == '__main__':
    app.run()
