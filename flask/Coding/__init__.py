from flask import Flask, g, render_template, Markup, request
import paramiko
import time
import os
import subprocess
import requests

app = Flask(__name__)
app.debug = True
# app.jinja_env.trim.blocks = True

class Ssh:
    Shell = None
    client = None
    transport = None

    def __init__(self, address, username, password):
        print("Connecting to server on ip", str(address) + ".")
        self.client = paramiko.client.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        self.client.connect(address, username=username, password=password)
        self.transport = paramiko.Transport((address, 22))
        self.transport.connect(username=username, password=password)
        self.sftp = paramiko.SFTPClient.from_transport(self.transport)

    def close_connection(self):
            if self.client is not None:
                self.client.close()
                self.sftp.close()
                self.transport.close()

    def open_shell(self):
        self.Shell = self.client.invoke_shell() 

    """def check_exist(self):
        self.Shell.send("isfile")
        """
    def mkfile_shell(self,file_name):
        if self.Shell:
            self.Shell.send("touch " + file_name + "\n")


    def send_shell(self, command):
        if self.Shell:
            self.Shell.send(command + "\n")
        else:
            print("Shell not opened.")

    def print_result(self):
        output = self.Shell.recv(65535).decode("utf-8")
        return output
    
    def create_file(self):
        ftp = self.client.open_sftp()
        my_file = ftp.file('/home/test1.py', 'w')
        my_file.write('print("Hello world")')
        my_file.flush()
        ftp.close()

url = 'http://192.168.0.96:8080/client/api'

@app.route('/')
def mainDisplay():
    username = 'Kim donghwan'
    return render_template('login.html', username=username)

@app.route('/login', methods=['POST'])
def login():
    userId = request.form['id']
    password = request.form['password']

    login_data = {'command':'login', 'username':userId, 'password':password, 'response':'json'}
    global user
    user = requests.Session()
    req = user.post(url, data=login_data)
    code = req.status_code
    # projectpath = request.form['projectFilePath']
    return render_template('re_test.html',code = code)

@app.route('/complete', methods=['POST'])
def complete():
    newId = request.form['newId']
    newPassword = request.form['newPassword']
    newEmail = request.form['newEmail']
    firstName = request.form['firstName']
    lastName = request.form['lastName']

    register_data = {'command':'createUser', 'account':'admin', 'username':newId, 'password':newPassword, 'email':newEmail, 'firstname':firstName,
    'lastname':lastName, 'response':'json'}
    # s=requests.Session()
    global user
    req = user.post(url, data=register_data)
    # email = req['email']
    code = req.status_code
    return render_template('complete.html', code=code)
# @app.route('/register')
# def registerPage():
#     return render_template('register.html')

@app.route('/create')
def createPage():
    return render_template('create.html')

@app.route('/editor')
def editorPage():
    return render_template('editor.html')

@app.route('/test')
def test():
    sshUsername = "root"
    sshPassword = "whfdjqrhkwp"
    sshServer = "192.168.0.184"

    connection = Ssh(sshServer, sshUsername, sshPassword)
    connection.open_shell()
    connection.send_shell("cd /home")
    connection.create_file()
    time.sleep(10)
    # print('==========================')
    result = connection.print_result()
    # connection.print_result()
    connection.close_connection()
    return render_template('test.html', result = result)

@app.route('/test2', methods=['POST'])
def test2():
    userName = request.form['userName']
    userEmail = request.form['userEmail']
    return render_template('test2.html', userName=userName, userEmail=userEmail)
# @app.before_request

# def before_request():
#     print("before_request")
#     g.str = "한글"

# @app.route("/tmpl")
# def t():
#     tit = Markup("<strong>Title<strong>")
#     mu = Markup("<h1>iii = <i>%s</i></h1>")
#     h = mu % "Italic"
#     print("h=", h)
#     return render_template('index.html', title = tit, mu = h)

# @app.route("/")
# def helloworld():
#     return "Hello Flask World!"

# @app.route("/gg")
# def helloworld2():
#     return "Hello Flask World!" + getattr(g, 'str', '111')


