import ssh_vm
import time
sshUsername = "root"
sshPassword = "whfdjqrhkwp"
sshServer = "192.168.0.150"

connection = ssh_vm.Ssh(sshServer, sshUsername, sshPassword)
# connection = Ssh(sshServer, sshUsername, sshPassword)
connection.open_shell()
# connection.send_command('mysql -uroot')
# connection.send_command('use user_info;')
connection.send_command('cd /home')
connection.print_result()
time.sleep(10)
print('==========================')
val = input("Enter your command: ")
connection.send_command(val)
connection.print_result()
val = input("Enter your command2: ")
connection.send_command(val)
connection.print_result()
connection.close_connection()