# Title  : Python 3 Simple Webserver
# Author : Ryan Carr
# Created: June 11, 2017
# Purpose: This program emulates a simple web server. It will open a port
#          then wait for an incomming connection from a browser. It will
#          send the contents of the webpage once, then shut down the server.
#          If you want to see the page again you'll need to rerun the program
#          and hit refresh on the browser window after the program is running.
from socket import *

# CONSTANTS
# Address 0.0.0.0 or an empty string is a multicast address.
# Meaning  all IP address on all Network Interface Cards in the server.

# This string can be changed, (it must remain a string), some other values
# you may want to try  localhost   127.0.0.1  and the ip you find in ipconfig
ADDRESS = '0.0.0.0'

# What port will you connect to the server on? Can be any number between
# 1 and 65535 If you want to know why that number feel free to ask
# (Keep in mind that ports below 1024 are reserved by the system)
# Standard ports for web connections are 80 and 8080, 443 is used for
# HTTPS secure connections
# NOTE: Setting the port to 443 does not automatically secure the connection
#       You would need to write a SSL wrapper or use a library for that.

# Feel free to change this integer to any number you want, if you plan to use
# something other than 80 or 8080 might I suggest a number between 3000 and
# 60000
PORT = 80

# Create a socket object, AF_INET means use IPv4 addressing
# SOCK_STREAM means the socket will be a TCP socket, not UDP.
sock = socket(family=AF_INET, type=SOCK_STREAM)

# Bind the socket to an IP ADDRESS / PORT pair.
sock.bind( (ADDRESS, PORT) )

# Listen for an incoming connection
sock.listen(1)

print("This webserver will continue to serve pages until you press CTRL+C")
print("It may appear the server is hanging after pressing Ctrl+C, if so")
print("try to connect to the webserver again with a web browser.")

try:
    while True:
    # Accept an incoming connection and create a client_connection object
    # also create a client_address object. The connection object is used
    # for communication between server and client
    # client_address is a string representation of the ip address the client
    # is connecting from
        client_connection, client_address = sock.accept()

    # Web browsers first send out a GET request, so we need to receive
    # that request or our webserver won't work properly

    # Python 3 sockets send and receive byte strings.
    # If wwe want to treat it as a normal string we will
    # need to decode it first.
        request = client_connection.recv(1024)
        print( "\nRequest data: ", request.decode() )

    # This is where the actual web page code goes. We can write it all inline
    # using ''' or """ to enclose the multiline string.
    # Another alternate is read the data in from the file.
        http_response = '''\
HTTP/1.1 200 OK

<html>
<body>
<h1>Hello World! </h1>
</body>
</html>
'''
    # In Python 3 byte strings are used for socket communication.
    # In order for us to send the string we created we need to encode it
    # into a byte string. You can either add a lowercase b before the string
    # or use the str.encode method. Encode converts a string to a UTF-8
    # byte string.
        client_connection.sendall( http_response.encode() )

    # It is vital to close the connection after we are through using
    # it. If we fail to close it the port is locked open and any other
    # programs that ask to use it will be refused.
        client_connection.close()

except KeyboardInterrupt:
    print("Closing server {0}/{1}".format(ADDRESS, PORT))
