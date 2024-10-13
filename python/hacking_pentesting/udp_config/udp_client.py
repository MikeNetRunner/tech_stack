import socket

target_host = '127.0.0.1'
target_port = 9997

#Create socket object
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#Send data
client.sendto("AAABBBCCC".encode(), (target_host,target_port))

#Get data
data, addr = client.recvfrom(4096)

print(data.decode())
client.close()