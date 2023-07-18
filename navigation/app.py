from flask import Flask, render_template, session, redirect, url_for, request

app = Flask(__name__)
app.secret_key = 'dummy_key'


@app.route('/')
def index():
    return redirect(url_for('home'))


@app.route('/home')
def home():
    if session['username']:
        return render_template('index.html', username=session['username'])
    else:
        return redirect(url_for('login'))

    
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        session['username'] = username
        return redirect(url_for('home'))
    return render_template('login.html')


@app.route('/explore')
def explore():
    if 'username' in session:
        return render_template('explore.html', username=session['username'])
    else:
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)