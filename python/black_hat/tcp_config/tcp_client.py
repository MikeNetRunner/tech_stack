import socket

target_host = '127.0.0.1'
target_port = 9998

#Create socket object
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Connection to server
client.connect((target_host,target_port))

#Send data
request = "Unauthorized device"
client.send(request.encode())

#Get data
response = client.recv(4096)

print(response.decode())
client.close()