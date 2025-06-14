import socket

# Define the server address and port
HOST = '127.0.0.1'  # Localhost
PORT = 8080         # Port of the server

# Create a client socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
client_socket.connect((HOST, PORT))

# Send a simple message to the server
message = "Hello, Server!"
client_socket.sendall(message.encode())

# Receive the server's response
response = client_socket.recv(1024).decode()
print("Server response:", response)

# Close the connection
client_socket.close()
