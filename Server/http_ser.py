import socket
import os
# Define host and port
HOST = '127.0.0.1'  # Localhost
PORT = 8080         # Port to listen on

# Create a TCP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)  # Allow multiple simultaneous connections
print(f"Server running on http://{HOST}:{PORT}/")

# Function to list all files in the current folder
def list_files():
    files = os.listdir(".")
    return files

while True:
    print("Waiting for a connection...")
    connection_socket, addr = server_socket.accept()
    print(f"Connection established with {addr}")

    try:
        # Receive the HTTP request
        request = connection_socket.recv(1024).decode()
        print("Request received:")
        print(request)

        # Parse the request to get the requested file
        request_lines = request.split('\r\n')
        if len(request_lines) > 0:
            filename = request_lines[0].split()[1]

        # Remove leading slash from filename
        if filename == "/":
            filename = "/index.html"
        filepath = filename.lstrip("/")

          # Check if the requested file exists or serve the file list
        if filepath == "list":
            file_list = list_files()
            content = """
            <html>
            <head>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        background-color: #f4f4f9;
                        margin: 0;
                        padding: 0;
                    }
                    h1 {
                        text-align: center;
                        color: #4a4a4a;
                        margin-top: 20px;
                    }
                    ul {
                        list-style-type: none;
                        padding: 0;
                        max-width: 600px;
                        margin: 20px auto;
                        background: #ffffff;
                        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                        border-radius: 10px;
                        overflow: hidden;
                    }
                    li {
                        padding: 15px 20px;
                        border-bottom: 1px solid #ddd;
                    }
                    li:last-child {
                        border-bottom: none;
                    }
                    a {
                        text-decoration: none;
                        color: #007bff;
                        font-size: 16px;
                    }
                    a:hover {
                        color: #0056b3;
                    }
                </style>
            </head>
            <body>
                <h1>File List</h1>
                <ul>
            """
            for file in file_list:
                content += f'<li><a href="{file}">{file}</a></li>'
            content += """
                </ul>
            </body>
            </html>
            """

            response = "HTTP/1.1 200 OK\r\n"
            response += "Content-Type: text/html\r\n\r\n"
            response += content

        # Check if the file is an image (e.g., .jpg, .png)
        elif filepath.endswith((".jpg", ".jpeg", ".png", ".gif")):
            try:
                with open(filepath, 'rb') as file:
                    content = file.read()

                # Create HTTP response with 200 OK
                response = "HTTP/1.1 200 OK\r\n"
                response += f"Content-Type: image/{filepath.split('.')[-1]}\r\n\r\n"
                connection_socket.sendall(response.encode() + content)
                continue  # Skip the default response handling

            except FileNotFoundError:
                response = "HTTP/1.1 404 Not Found\r\n"
                response += "Content-Type: text/html\r\n\r\n"
                response += "<html><body><h1>404 Not Found</h1></body></html>"

        else:
            try:
                # Try to open the requested file
                with open(filepath, 'r') as file:
                    content = file.read()

                response = "HTTP/1.1 200 OK\r\n"
                response += "Content-Type: text/html\r\n\r\n"
                response += content

            except FileNotFoundError:
            # File not found, return 404 response
                response = "HTTP/1.1 404 Not Found\r\n"
                response += "Content-Type: text/html\r\n\r\n"
            #response += "<html><body><h1>404 Not Found</h1></body></html>"
                response += """
<html>
<head>
    <style>
        body {
            font-family: 'Arial', sans-serif;
            background-color: #f4f4f9;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        .error-container {
            text-align: center;
            background-color: #fff;
            border-radius: 15px;
            padding: 50px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            max-width: 500px;
            width: 100%;
            transition: transform 0.3s ease;
        }
        .error-container:hover {
            transform: scale(1.05);
        }
        .error-code {
            font-size: 100px;
            color: #e74c3c;
            font-weight: bold;
        }
        .error-message {
            font-size: 24px;
            color: #34495e;
            margin-bottom: 20px;
        }
        .home-link {
            font-size: 18px;
            color: #3498db;
            text-decoration: none;
            border: 2px solid #3498db;
            padding: 10px 20px;
            border-radius: 5px;
            transition: background-color 0.3s;
        }
        .home-link:hover {
            background-color: #3498db;
            color: #fff;
        }
        .error-image {
            margin-top: 30px;
            width: 150px;
            height: 150px;
            background-image: url('https://www.clipartmax.com/png/full/28-281610_404-error-page-not-found.jpg');
            background-size: cover;
            background-position: center;
            border-radius: 50%;
            margin: 0 auto;
        }
    </style>
</head>
<body>
    <div class="error-container">
        <div class="error-code">404</div>
        <div class="error-message">Oops! The page you're looking for cannot be found.</div>
        <img src="https://static.vecteezy.com/system/resources/previews/017/388/362/non_2x/faulty-broken-robot-emits-electrical-discharges-isolated-illustration-vector.jpg" width="200" height="200">
        <div class="error-image"></div>
    </div>
</body>
</html>
"""

        # Send the HTTP response
        connection_socket.sendall(response.encode())

    except Exception as e:
        print(f"Error processing request: {e}")
    finally:
        # Close the connection socket
        connection_socket.close()
        print("Connection closed.")

    # Exit after handling one request

# Clean up the server socket
server_socket.close()
