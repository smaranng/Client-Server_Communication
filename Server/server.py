import socket

# Define host and port
HOST = '127.0.0.1'  # Localhost
PORT = 8080         # Port to listen on

# Create and configure the server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)
print(f"Server running on {HOST}:{PORT}")

# Accept a connection from the client
connection_socket, addr = server_socket.accept()
print(f"Connection established with {addr}")

# Receive the message from the client
message = connection_socket.recv(1024).decode()
print("Received message:", message)

response='Hello Client!'
# Send a response back to the client
response = "Received message: " + response
connection_socket.sendall(response.encode())

# Close the connection
connection_socket.close()
print("Connection closed.")
