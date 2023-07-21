from flask import Flask, render_template, request, url_for, redirect
#import splite3

app = Flask(__name__)

@app.route('/')
def index():
    text = request.args.get("text", "")

    return (
        """<form action="" method="get">
                Enter Text: <input type="text" name="text">
                <input type="submit" value="Go!">
            </form>"""
        + "Text: "
        + text 
    )


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)

