import paramiko
import time
import os
import subprocess


class Ssh:
    Shell = None
    client = None
    transport = None
    ftp = None

    def __init__(self, address, username, password):
        print("Connecting to server on ip", str(address) + ".")
        self.client = paramiko.client.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        self.client.connect(address, username=username, password=password)
        self.transport = paramiko.Transport((address, 22))
        self.transport.connect(username=username, password=password)
        self.sftp = paramiko.SFTPClient.from_transport(self.transport)

    def close_connection(self):
        try:
            self.client.close()
            self.sftp.close()
            self.transport.close()
        except Exception as e:
            print(str(e))

    def open_shell(self):
        try:
            self.Shell = self.client.invoke_shell()
        except Exception as e:
            print(str(e))

    def mv_dir(self, path):
        try:
            self.Shell.send("cd " + path + "\n")
        except Exception as e:
            print(str(e))

    def put_file(self, lpath, rpath, file_name):
        try:
            local_path = lpath + '/' + file_name
            remote_path = rpath + '/' + file_name
            self.sftp.put(remote_path, local_path)
        except Exception as e:
            print(str(e))

    def get_file(self, lpath, rpath, file_name):
        try:
            local_path = lpath + '/' + file_name
            remote_path = rpath + '/' + file_name
            self.sftp.get(remote_path, local_path)
        except Exception as e:
            print(str(e))

    def f_write(self, path, file_name, contents):
        try:
            ftp = self.sftp.open(path + '/' + file_name, "w")
            ftp.write(contents)
            ftp.flush()
            ftp.close()
        except Exception as e:
            print(str(e))

    def show_code(self, path, file_name):
        try:
            ftp = self.sftp.open(path + '/' + file_name, 'r')
            result = ftp.read()
            print(result)
            ftp.flush()
            ftp.close()
        except Exception as e:
            print(str(e))

    def run_cfile(self, file_name):
        try:
            self.Shell.send("gcc " + file_name + " -o " + file_name + ".out\n")
            self.Shell.send("./" + file_name + ".out\n")
        except Exception as e:
            print(str(e))

    def run_pyfile(self, file_name):
        try:
            self.Shell.send("python " + file_name + "\n")
        except Exception as e:
            print(str(e))

    def send_command(self,command):
        try:
            self.Shell.send(command + '\n')
        except Exception as e:
            print(str(e))

    def print_result(self):
        try:
            output = self.Shell.recv(65535).decode("utf-8"
                                                   )
            print(output)
        except Exception as e:
            print(str(e))
            
    def output(self):
        try:
            return self.Shell.recv(65535).decode("utf-8")
        except Execption as e:
            print(str(e))


# sshUsername = "root"
# sshPassword = "whfdjqrhkwp"
# sshServer = "192.168.0.150"

# connection = Ssh(sshServer, sshUsername, sshPassword)
# connection.open_shell()
# connection.send_command('cd /home')
# connection.send_command('use user_info;')
# connection.send_command('select * from user_code;')

# time.sleep(10)
# print('==========================')
# connection.print_result()
# connection.close_connection()

#connection.get_file('C:/Users/Public/Documents/PythonProject', '/home/user', 'hello.c')
#connection.show_code('/home/user', 'test.py')
#connection.send_command('ls -a')
#connection.f_write('/home/user', 'test2.py', 'print("this is test file2")')

#connection.send_command('CREATE TABLE user_code (user_id varchar(30),user_code longtext);')
#connection.send_command('grant all privileges on *.* to root@192.168.0.92 identified by "123456";')
