# Multi-Threaded Web Server and FTP Client

## Overview

This repository contains an implementation of a multi-threaded web server and an FTP client. The project is divided into two main tasks:

1. **Task 1:** Implement a multi-threaded web server in Python.
2. **Task 2:** Extend the web server to act as an FTP client to download text files from a local FTP server.

## Getting Started

### Prerequisites

- Python 3.x
- Docker (for setting up the FTP server)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/qme02/Multi-Threaded-Web-Server-and-FTP-Client
   cd Multi-Threaded-Web-Server-and-FTP-Client

### Docker Setup for FTP Server

1. **Install Docker:**
   - Follow the [official Docker installation guide](https://docs.docker.com/get-docker/) for your operating system.

2. **Run the Docker container for the FTP server:**
   ```bash
   docker run --rm -it -p 20:20 -p 21:21 -p 4559-4564:4559-4564 -e FTP_USER=1234 -e FTP_PASSWORD=1234 docker.io/panubo/vsftpd:latest

3. **List running Docker containers to find the container ID in a new terminal window:**
   ```bash
   docker container ls

4. **Log in to the container and change ownership of the FTP directory:**
  - Replace <CONTAINER_ID> with the actual container ID from the previous step.
     ```bash
     docker exec -it <CONTAINER_ID> /bin/bash
  - Inside the container, change the ownership of the FTP directory:
    ```bash
     chown ftp:ftp /srv

5. **Create a test file in the FTP directory:**
  - Still inside the container, create a test file:
    ```bash
    echo "Hello World!" >> /srv/ftp_test.txt

6. **Verify setup by accessing files through the web server:**
  - In your web browser, navigate to the following URLs to test various content types:
    - http://localhost:6789/index.html
    - http://localhost:6789/index2.html
    - http://localhost:6789/index.txt
    - http://localhost:6789/index.png
    - http://localhost:6789/index.jpg
    - http://localhost:6789/index.jpeg
    - http://localhost:6789/index.gif
    - http://localhost:6789/ftp_test.txt (This will test the FTP client functionality)
