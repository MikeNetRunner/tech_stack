import socket
import ssl

target_host = 'tickets.pionier.gov.pl'  # Correct host without protocol
target_port = 443  # Use 443 for HTTPS

# Create a socket object
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Create an SSL context
context = ssl.create_default_context()

# Wrap the socket with the SSL context
client = context.wrap_socket(client, server_hostname=target_host)

# Connect to the server
client.connect((target_host, target_port))

# Send an HTTP GET request
request = "GET /public/ HTTP/1.1\r\nHost: tickets.pionier.gov.pl\r\nConnection: close\r\n\r\n"
client.send(request.encode())

# Get data
response = b""
while True:
    part = client.recv(4096)
    if not part:
        break
    response += part

# Decode and print the complete response
print(response.decode())

# If you only want the body content, you can do this:
response_str = response.decode()
# Find the start of the body by splitting on double CRLF
body_start = response_str.find("\r\n\r\n") + 4  # Move past the headers
body = response_str[body_start:]  # Get the body content
print(body)  # Print just the HTML body

client.close()
