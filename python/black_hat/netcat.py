import argparse
import socket
import shlex
import subprocess
import sys
import textwrap
import threading

# Function to execute a shell command
def execute(cmd):
    cmd = cmd.strip()  # Remove leading/trailing spaces from the command
    
    if not cmd:
        return  # If command is empty, return
    
    # Execute the command and capture its output
    output = subprocess.check_output(shlex.split(cmd), stderr=subprocess.STDOUT)
    return output.decode()  # Return the decoded output


# Define a class to handle the NetCat tool
class NetCat:
    def __init__(self, args, buffer=None):
        # Store arguments and the optional buffer to send
        self.args = args
        self.buffer = buffer
        
        # Create a TCP socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Set socket options to reuse the address if in use
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


    # Main entry point to either send or listen based on provided arguments
    def run(self):
        if self.args.listen:
            # If in listen mode, start listening for connections
            self.listen()
        else:
            # Otherwise, send data to the target
            self.send()


    # Function to handle sending data to the server
    def send(self):
        # Connect to the server at the given target IP and port
        self.socket.connect((self.args.target, self.args.port))
        
        # If a buffer was passed, send it to the server
        if self.buffer:
            self.socket.send(self.buffer)

        try:
            # Enter a loop to continuously receive and send data
            while True:
                recv_len = 1
                response = ''
                
                # Keep receiving data from the server
                while recv_len:
                    data = self.socket.recv(4096)  # Receive data in chunks of 4096 bytes
                    recv_len = len(data)
                    response += data.decode()  # Decode the received data
                    
                    if recv_len < 4096:
                        # If less than 4096 bytes are received, end the receiving loop
                        break

                if response:
                    # Print the server response
                    print(response)
                    
                    # Input data to send back to the server
                    buffer = input('> ')
                    buffer += '\n'  # Append a newline character
                    self.socket.send(buffer.encode())  # Send the input data back to the server
        
        except KeyboardInterrupt:
            # If the user interrupts with Ctrl+C, handle it gracefully
            print('KeyboardInterrupt by User')
            self.socket.close()  # Close the socket
            sys.exit()  # Exit the program


    # Function to handle listening for incoming connections
    def listen(self):
        print('Listening')
        # Bind the socket to the given target IP and port
        self.socket.bind((self.args.target, self.args.port))
        
        # Start listening for incoming connections (up to 5 queued connections)
        self.socket.listen(5)
        
        while True:
            # Accept incoming connections
            client_socket, _ = self.socket.accept()
            
            # Create a new thread to handle the client connection
            client_thread = threading.Thread(target=self.handle, args=(client_socket,))
            client_thread.start()


    # Function to handle client connection
    def handle(self, client_socket):
        if self.args.execute:
            # If an execute argument was provided, run the command
            output = execute(self.args.execute)
            # Send the output back to the client
            client_socket.send(output.encode())
        
        elif self.args.upload:
            # If an upload argument was provided, handle file upload
            file_buffer = b''  # Buffer to hold the received file data
            
            while True:
                data = client_socket.recv(4096)  # Receive data in chunks
                if data:
                    file_buffer += data  # Append received data to the buffer
                else:
                    break  # If no more data, exit the loop
            
            # Write the received data to the specified file
            with open(self.args.upload, 'wb') as f:
                f.write(file_buffer)
            
            # Send a confirmation message back to the client
            message = f'Saved file: {self.args.upload}'
            client_socket.send(message.encode())

        elif self.args.command:
            # If in command mode, open an interactive command shell
            cmd_buffer = b''  # Buffer to hold the command input
            
            while True:
                try:
                    # Send a command prompt to the client
                    client_socket.send(b' #> ')
                    
                    # Keep receiving command input from the client
                    while '\n' not in cmd_buffer.decode():
                        cmd_buffer += client_socket.recv(4096)
                    
                    # Execute the received command
                    response = execute(cmd_buffer.decode())
                    
                    if response:
                        # Send the command output back to the client
                        client_socket.send(response.encode())
                    cmd_buffer = b''  # Clear the buffer after sending the output
                
                except Exception as e:
                    # If an error occurs, handle it and close the socket
                    print(f'Server stopped {e}')
                    self.socket.close()
                    sys.exit()


# Entry point of the script when executed from the command line
if __name__ == '__main__':
    # Create a command-line argument parser
    parser = argparse.ArgumentParser(
        description='NetCat tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent('''Examples:
                               netcat.py -t <IP> -p <PORT> -l c #Bash
                               netcat.py -t <IP> -p <PORT> -l -u=mytest.whatisup #Load files
                               netcat.py -t <IP> -p <PORT> -l -e="cat /etc/passwd" #Run command
                               echo 'MESSAGE' | ./netcat.py -t <IP> -p <PORT> #Send text to server on <IP> by <PORT>
                               netcat.py -t <IP> -p <PORT> #Connection to server''')
    )
    
    # Define command-line arguments
    parser.add_argument('-c', '--command', action='store_true', help='open bash')
    parser.add_argument('-e', '--execute', help='run command')
    parser.add_argument('-l', '--listen', action='store_true', help='listening')
    parser.add_argument('-p', '--port', type=int, default=5555, help='destination port')
    parser.add_argument('-t', '--target', default='0.0.0.0', help='destination IP address')
    parser.add_argument('-u', '--upload', help='load file')
    
    # Parse the provided arguments
    args = parser.parse_args()

    # If in listening mode, set buffer to empty, otherwise read input from stdin
    if args.listen:
        buffer = ''
    else:
        buffer = sys.stdin.read()

    # Initialize the NetCat instance with parsed arguments and buffer
    nc = NetCat(args, buffer.encode('utf-8'))
    nc.run()
