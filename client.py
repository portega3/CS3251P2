import socket

host = socket.gethostname()
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host, 50000))
while 1:
    # msg = raw_input("SEND>> ")
    # msg = client_socket.recv(1024)
    # client_socket.send(msg)
    data = client_socket.recv(1024)
    if ( data == 'q' or data == 'Q'):
        print("Error: Too Many Clients Already Connected YOU FUCK")
        client_socket.close()
        break;
    else:
        print "RECIEVED:" , data
        data = raw_input ( "SEND( TYPE q or Q to Quit):" )
        if (data <> 'Q' and data <> 'q'):
            client_socket.send(data)
        else:
            client_socket.send(data)
            client_socket.close()
            break;
