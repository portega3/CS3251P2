import socket               # Import socket module
import thread
import random
import sys

class ClientSupervisor:
    def __init__(self):
        self.num_clients = 0
        self.word_list = []
    def add_client(self):
        self.num_clients += 1
    def close_client(self):
        self.num_clients -= 1
    def get_num_clients(self):
        return self.num_clients

def on_new_client(clientsocket,addr, word):

    global supervisor
    # supervisor.add_client()
    msg = clientsocket.send("OK")
    msg = clientsocket.recv(1024)
    msg_length, msg = msg.split("/")

    # print("msg_length: %s, msg: %s" % (msg_length, msg))

    if msg == "OK":
        # print("Connection Successful")
        isRunning = True
        print("The word for this sucker is " + word)
        incorrect_guesses = ""
        num_incorrect_guesses = 0
        current_guesses = []

        return_string, current_guesses, is_correct, all_correct = check_guess(word, [], [], initializing=True)
        msg = ("/").join([str(return_string), str(incorrect_guesses), str(is_correct), str(all_correct)])
        clientsocket.send(msg)
    else:
        # print("Connectioon Failed, Terminating Connection")
        isRunning = False

    # word = random.choice(supervisor.word_list).lower()

    # print("here?")

    # isRunning = True
    while isRunning:
        msg = clientsocket.recv(1024)
        msg_length, guess = msg.split("/")
        # print("\nGuess on this end: %s" % str(guess))
        return_string, current_guesses, is_correct, all_correct = check_guess(word, current_guesses, guess)
        # print("Is Correct guess: %s" % str(is_correct))

        if all_correct:
            # print("Victor!")
            isRunning = False
            msg = ("/").join([str(return_string), str(incorrect_guesses), str(is_correct), str(all_correct)])

        elif not is_correct:
            incorrect_guesses = incorrect_guesses + guess
            num_incorrect_guesses += 1
            msg = ("/").join([str(return_string), str(incorrect_guesses), str(is_correct), str(all_correct)])

            # print("Found Incorrect Guess")
        elif is_correct:
            # print("Found Correct Guess")
            msg = ("/").join([str(return_string), str(incorrect_guesses), str(is_correct), str(all_correct)])
        # if isRunning:
        if num_incorrect_guesses >= 6:
            isRunning = False
            msg = ("/").join(["$INCORRECT$", " ", " ", " "])
            clientsocket.send(msg)
        else:
            clientsocket.send(msg)

    supervisor.close_client()
    clientsocket.close()

def check_guess(correct_word, current_guesses, guess, initializing=False):
    is_correct = False
    return_string = ""
    num_correct = 0
    # print("guess: %s" % guess)
    if initializing == True:
        for x in range(len(correct_word)):
            return_string = return_string +  "_ "
    else:
        current_guesses.append(guess)
        for letter in list(correct_word):
            if letter in current_guesses:
                return_string = return_string + "{} ".format(letter)
                num_correct += 1
                if letter == guess:
                    is_correct = True
            else:
                return_string = return_string + "_ "

    if num_correct == len(correct_word):
        all_correct = True
    else:
        all_correct = False
    return return_string[:-1], current_guesses, is_correct, all_correct

def deny_new_client(clientsocket,addr):

    msg = clientsocket.send("q")
    # msg = clientsocket.rcv(1024)
    #do some checks and if msg == someWeirdSignal: break:
    #
    #     print(addr, ' >> ', msg)
    #     msg = raw_input('SERVER >> ')
    #     #Maybe some code to compute the last digit of PI, play game or anything else can go here and when you are done.
    #     clientsocket.send(msg)
    # supervisor.num_clients -= 1
    clientsocket.close()

def open_file(filename):
    words = []
    with open(filename, 'r') as fh:
        for line in fh:
            words.append(line.rstrip('\n'))

    words = words[1:]
    return words

def main(port):
    s = socket.socket()         # Create a socket object
    host = socket.gethostname() # Get local machine name
                  # Reserve a port for your service.

    #Starting Supervisor
    global supervisor
    #Loading File


    print('Server started!')
    print('Waiting for clients...')



    s.bind((host, port))        # Bind to the port
    s.listen(5)                 # Now wait for client connection.

    isRunning = True
    while isRunning:
        print("Num Clients: %s" % str(supervisor.get_num_clients()))
        # num_clients = supervisor.num_clients
        # print("num_clients: %s" % str(num_clients))
        if supervisor.get_num_clients() < 3:
            # supervisor.num_clients += 1
            supervisor.add_client()
            c, addr = s.accept()     # Establish connection with client.
            print('Got connection from', addr)
            word = random.choice(supervisor.word_list).lower()
            thread.start_new_thread(on_new_client,(c,addr,word))
            print("Handling thread started")
            #Note it's (addr,) not (addr) because second parameter is a tuple
            #Edit: (c,addr)
            #that's how you pass arguments to functions when creating new threads using thread module.
            # if supervisor.num_clients == 2:
            #     isRunning = False
        else:
            c, addr = s.accept()
            thread.start_new_thread(deny_new_client, (c, addr))
            #Send some signal to refuse the client.
    s.close()

if __name__ == "__main__":
    # num_clients = 0
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    else:
        port = 50000
    global supervisor
    supervisor = ClientSupervisor()
    supervisor.word_list = open_file('words.txt')
    print("supervisor.word_list" + str(supervisor.word_list))
    main(port)
