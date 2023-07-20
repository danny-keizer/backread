from flask import Flask, send_from_directory, request, Response, redirect
import os
import socket
import subprocess
import sys


def install_modules(modules):
    for module in modules:
        try:
            __import__(module)
        except ImportError:
            subprocess.check_call([sys.executable, "-m", "pip", "install", module])


modules = ["flask", "socket", "gunicorn"]
install_modules(modules)

# Find IP address
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(('8.8.8.8', 80))
local_ip = s.getsockname()[0]
s.close()

# General options
ww = "honeybee2000!"
app = Flask(__name__)


@app.route('/<path:path>')
def send_file(path):
    return send_from_directory(os.getcwd(), path)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form['password']
        if password == ww:
            resp = redirect('/')
            resp.set_cookie('password', password)
            return resp
        else:
            return redirect('/login')
    return '''
        <html>
            <head>
                <link rel="stylesheet" href="css/login.css">
            </head>
            <body>
                <form method="post">
                    <label for="password">Password:</label><br>
                    <input type="password" id="password" name="password"><br><br>
                    <input type="submit" value="Login">
                    <span>I Love you Marianne &#128151; </span><br><br>
                </form>
            </body>
        </html>
    '''


@app.route('/')
def index():
    password = request.cookies.get('password')
    if not password or password != ww:
        return redirect('/login')
    # Your protected content here
    return send_from_directory(os.getcwd(), 'messages.html')


if __name__ == '__main__':
    context = ('ssl/cert.pem', 'ssl/key.pem')
    app.run(host=f"{local_ip}") #ssl_context=context,
