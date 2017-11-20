import socket               # Import socket module
import thread

class ClientSupervisor:
    def __init__(self):
        self.num_clients = 0


def on_new_client(clientsocket,addr, supervisor):
    isRunning = True
    while isRunning:
        msg = clientsocket.send("OK")
        msg = clientsocket.recv(1024)
        #do some checks and if msg == someWeirdSignal: break:
        if msg == "Q":
            isRunning = False
        else:
            print(addr, ' >> ', msg)
            msg = raw_input('SERVER >> ')
            #Maybe some code to compute the last digit of PI, play game or anything else can go here and when you are done.
            clientsocket.send(msg)
    supervisor.num_clients -= 1
    clientsocket.close()


def deny_new_client(clientsocket,addr):

    msg = clientsocket.send("q")
    #do some checks and if msg == someWeirdSignal: break:
    #
    #     print(addr, ' >> ', msg)
    #     msg = raw_input('SERVER >> ')
    #     #Maybe some code to compute the last digit of PI, play game or anything else can go here and when you are done.
    #     clientsocket.send(msg)
    # supervisor.num_clients -= 1
    clientsocket.close()

def main():
    s = socket.socket()         # Create a socket object
    host = socket.gethostname() # Get local machine name
    port = 50000                # Reserve a port for your service.

    print('Server started!')
    print('Waiting for clients...')

    supervisor = ClientSupervisor()

    s.bind((host, port))        # Bind to the port
    s.listen(5)                 # Now wait for client connection.


    while True:
        print("Num Clients: %s" % str(supervisor.num_clients))
        if supervisor.num_clients < 3:
            c, addr = s.accept()     # Establish connection with client.
            print('Got connection from', addr)
            supervisor.num_clients += 1
            thread.start_new_thread(on_new_client,(c,addr,supervisor))
            print("Handling thread started")
            #Note it's (addr,) not (addr) because second parameter is a tuple
            #Edit: (c,addr)
            #that's how you pass arguments to functions when creating new threads using thread module.
        else:
            c, addr = s.accept()
            thread.start_new_thread(deny_new_client, (c, addr))
            #Send some signal to refuse the client.
    s.close()

if __name__ == "__main__":
    main()
