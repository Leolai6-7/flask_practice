# 引入模組

from flask import Flask

app = Flask(__name__)
@app.route('/<name>')
def home(name):
    return f"{name},Welcome,this is Home Page"

@app.route("/hello")
def hello():
    return "Hello World! This is Hello Page "

if __name__ == '__main__':
    app.run()