import socket

host = socket.gethostname()
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host, 50000))

data = client_socket.recv(1024)
if data == "OK":
    print("Welcome to Hangman!")
    raw_input("Press ENTER TO BEGIN")
    msg = "OK"
    msg = client_socket.send(msg)
elif data == 'q' or data == 'Q':
    print("Error: Too Many Clients Already Connected")
    client_socket.close()


msg = client_socket.recv(1024)
word, incorrect_guesses, _, _ = msg.split("/")
print(word)
# print("Incorrect Guesses: %s" % str(incorrect_guesses))
isRunning = True
while isRunning:
    guess = raw_input("Please Enter a Guess\n$").lower()

    if guess.isalpha():

        msg = client_socket.send(guess.lower())

        msg = client_socket.recv(1024).split("/")
        print("Received Message here: %s" % str(msg))

        word = msg[0]
        incorrect_guesses = msg[1]
        is_correct = msg[2]
        all_correct = msg[3]

        # print("Received Message here: %s" % str(msg))

        print("***************************")
        if is_correct == "True":
            print("Great Guess!")
            if all_correct == "True":
                print("Victor!")
                isRunning = False
        else:
            print("Wrong!")

        print(word)
        print("Incorrect Guesses: %s" % str(incorrect_guesses))
        print("***************************")

        # msg = raw_input("SEND>> ")
        # msg = client_socket.recv(1024)
        # client_socket.send(msg)
        # data = client_socket.recv(1024)
        # if ( data == 'q' or data == 'Q'):
        #     print("Error: Too Many Clients Already Connected")
        #     client_socket.close()
        #     break;
        # else:
        #     print "RECIEVED:" , data
        #     data = raw_input ( "SEND( TYPE q or Q to Quit):" )
        #     if (data <> 'Q' and data <> 'q'):
        #         client_socket.send(data)
        #     else:
        #         client_socket.send(data)
        #         client_socket.close()
        #         break
    else:
        print("Please Write a Letter!")

client_socket.close()
