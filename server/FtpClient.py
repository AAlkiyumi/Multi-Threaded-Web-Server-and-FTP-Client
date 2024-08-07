import socket
import re

## @author Almaamar Alkiyumi


class FtpClient:
    CRLF = "\r\n"
    DEBUG = False  # Debug Flag

    def __init__(self):
        self.control_socket = None
        self.control_reader = None
        self.control_writer = None
        self.current_response = None

    def connect(self, hostname, port=21):
        try:
            # Establish the control socket
            self.control_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.control_socket.connect((hostname, port))

            # Get references to the socket input and output streams
            self.control_reader = self.control_socket.makefile('r')
            self.control_writer = self.control_socket.makefile('w')

            # Check if the initial connection response code is OK
            if self.check_response(220):
                print("Successfully connected to FTP server")

        except socket.error as e:
            print(f"Socket error: {e}")

    def login(self, username, password):
        try:
            # Send user name and password to FTP server
            self.send_command(f"USER {username}")
            self.send_command(f"PASS {password}")

        except socket.error as e:
            print(f"Socket error: {e}")

    def send_command(self, command):
        try:
            if self.control_writer is not None:
                # Send command to the FTP server
                self.control_writer.write(command + self.CRLF)
                self.control_writer.flush()
    
                # Get response from FTP server
                response = self.control_reader.readline().strip()
                if self.DEBUG:
                    print(f"Current FTP response: {response}")
    
                return response
            else:
                print("Control writer is not initialized.")
                return None
    
        except socket.error as e:
            print(f"Socket error: {e}")
        return None

    def check_response(self, expected_code):
        try:
            response = self.control_reader.readline().strip()
            if self.DEBUG:
                print(f"Current FTP response: {response}")

            if not response.startswith(str(expected_code)):
                return False

            return True

        except socket.error as e:
            print(f"Socket error: {e}")
            return False

    def enter_passive_mode(self):
        try:
            response = self.send_command("PASV")
            if response:
                data_port = self.extract_data_port(response)
                if self.DEBUG:
                    print(f"Data Port: {data_port}")
                return data_port
            else:
                return None

        except socket.error as e:
            print(f"Socket error: {e}")
            return None

    def extract_data_port(self, response_line):
        try:
            # Extract the data port number from the PASV response
            match = re.search(r'(\d+),(\d+),(\d+),(\d+),(\d+),(\d+)', response_line)
            if match:
                port_parts = match.groups()
                data_port = int(port_parts[4]) * 256 + int(port_parts[5])
                if self.DEBUG:
                    print(f"Port integers: {port_parts[4]}, {port_parts[5]}")
                return data_port
            else:
                return None

        except ValueError as e:
            print(f"ValueError: {e}")
            return None

    def retrieve_file(self, file_name):
        try:
            # Change to the current (root) directory first
            self.send_command(f"CWD /")

            # Set passive mode and retrieve the data port number
            data_port = self.enter_passive_mode()
            if data_port is not None:
                data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                data_socket.connect((self.control_socket.getpeername()[0], data_port))

                data_reader = data_socket.makefile('rb')
                self.send_command(f"RETR {file_name}")
                self.receive_file(data_reader, file_name)

                data_socket.close()

        except socket.error as e:
            print(f"Socket error: {e}")

    def receive_file(self, data_reader, file_name):
        try:
            with open(file_name, 'wb') as local_file:
                while True:
                    data = data_reader.read(1024)
                    if not data:
                        break
                    local_file.write(data)

            print(f"File '{file_name}' downloaded successfully")

        except IOError as e:
            print(f"IOError: {e}")

    def disconnect(self):
        try:
            self.send_command("QUIT")
            self.control_socket.close()
            print("Disconnected from FTP server")

        except socket.error as e:
            print(f"Socket error: {e}")


if __name__ == "__main__":
    ftp_client = FtpClient()
    ftp_client.connect("localhost")
    ftp_client.login("1234", "1234")
    ftp_client.retrieve_file("ftp_test.txt")
    ftp_client.disconnect()
