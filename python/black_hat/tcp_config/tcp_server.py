import socket  # Import the socket module for network communication
import threading  # Import threading module to handle multiple clients concurrently

# Define the IP address and port to bind the server
bind_ip = '127.0.0.1'  # Localhost IP address
bind_port = 9998  # Port number for the server to listen on


def main():
    """
    Main function to set up and run the TCP server.
    It listens for incoming connections and starts a new thread for each client.
    """
    # Create a TCP socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Bind the socket to the specified IP address and port
    server.bind((bind_ip, bind_port))
    
    # Start listening for incoming connections (max 5 queued connections)
    server.listen(5)
    print(f'[*] Listening on {bind_ip}:{bind_port}')  # Print a message indicating the server is listening

    while True:
        # Accept an incoming connection from a client
        client, address = server.accept()
        print(f'[*] Connection accepted from {address[0]}:{address[1]}')  # Log the client's address
        # Start a new thread to handle the client
        client_handler = threading.Thread(target=handle_client, args=(client,))
        client_handler.start()  # Start the thread


def handle_client(client_socket):
    """
    Handles communication with a connected client.

    Args:
        client_socket (socket.socket): The socket object for the client connection.
    """
    with client_socket as sock:
        # Receive up to 1024 bytes of data from the client
        request = sock.recv(1024)
        print(f'[*] Received: {request.decode("UTF-8")}')  # Print the received data
        # Send a response back to the client
        sock.send(b'Wrong way!')  # Send a simple message


if __name__ == '__main__':
    # Entry point of the script
    main()  # Call the main function to start the server
