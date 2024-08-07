# Import necessary modules
from socket import *
import sys
from ftplib import FTP


## @author Almaamar Alkiyumi



# FTP server configuration
ftp_server = 'localhost'
ftp_username = '1234'
ftp_password = '1234'

# Create an FTP connection
ftp = FTP(ftp_server)
ftp.login(user=ftp_username, passwd=ftp_password)

# Create a TCP server socket
serverSocket = socket(AF_INET, SOCK_STREAM)

# Assign a port number
serverPort = 6789

# Bind the socket to server address and server port
serverSocket.bind(("", serverPort))

# Listen to at most 1 connection at a time
serverSocket.listen(1)

# Define the content types for known file extensions
def contentType(fileName):
    if fileName.endswith(".html"):
        return "text/html"
    elif fileName.endswith(".txt"):
        return "text/plain"
    elif fileName.endswith(".jpg") or fileName.endswith(".jpeg"):
        return "image/jpeg"
    elif fileName.endswith(".gif"):
        return "image/gif"
    elif fileName.endswith(".png"):
        return "image/png"
    else:
        return "application/octet-stream"

# Server should be up and running and listening to incoming connections
while True:
    print('The server is ready to receive')

    # Set up a new connection from the client
    connectionSocket, addr = serverSocket.accept()

    try:
        # Receive the request message from the client
        message = connectionSocket.recv(1024).decode()
        print('Request:\n------------\n', message)

        # Extract the path of the requested object from the message
        filename = message.split()[1]
        # Remove the leading '/' from the filename
        filename = filename[1:]
        
        try:
            with open(filename, 'rb') as file:   # Check if the requested file exists locally
                # Read the content of the requested file
                outputdata = file.read()
        except FileNotFoundError:
            # If the file is not found locally, try to fetch it from FTP server
            try:
                # Check if the file exists on the FTP server before downloading it
                if filename in ftp.nlst():
                    with open(filename, 'wb') as file:
                        ftp.retrbinary('RETR ' + filename, file.write)
                    with open(filename, 'rb') as file:
                        outputdata = file.read()
                else:
                    # If the file is not found on the FTP server, return a 404 response
                    response = "HTTP/1.1 404 Not Found\r\n\r\n"
                    connectionSocket.send(response.encode())
                    connectionSocket.send("<html><head><title>404 Not Found</title></head><body><h1>404 Not Found</h1></body></html>\r\n".encode())
                    print('Response:\n------------\n', response)
                    connectionSocket.close()
                    continue
            except Exception as e:
                print("Error:", e)


        # Determine the content type using the contentType() method
        content_type = contentType(filename)
        # Send the HTTP response header line to the connection socket
        response = f"HTTP/1.1 200 OK\r\nContent-Type: {content_type}\r\n\r\n"
        connectionSocket.send(response.encode())
        # Send the content of the requested file to the connection socket
        connectionSocket.sendall(outputdata)
        print('Response:\n------------\n', response)  

        # Close the client connection socket
        connectionSocket.close()

    except Exception as e:
        print("Error:", e)

# Close the server socket
serverSocket.close()
sys.exit()  # Terminate the program after serving the corresponding data
