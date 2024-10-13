import socket

# Create a UDP socket
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the address and port
server.bind(('127.0.0.1', 9997))

print("Server UDP is up...")

while True:
    # Receive data from client
    data, addr = server.recvfrom(4096)
    print(f"Get data: {data.decode()} from {addr}")
    
    # Send response back to the client (using UTF-8 encoding)
    response = "Response from server"
    server.sendto(response.encode('utf-8'), addr)  # Encode to bytes
