import socket
import time
import sys

def echo(string, indent=1):  # name it whatever you want, e.g. p
    print('\t'*indent + string)

def draw_hangman(misses):
    echo('_____')
    echo('|    |')
    if misses >= 1:
        echo('|    O')
    else:
        echo('|')
    two_misses = '|'
    three_misses = '/|'
    four_misses = '/|\\'
    if misses >= 2:
        if misses > 4:
            body_misses = 4
        else:
            body_misses = misses
        miss_vector_body = ["",two_misses, three_misses, four_misses]

        body_shown = miss_vector_body[body_misses-1]
        if body_misses >= 3:
            body_spaces = 3
        else:
            body_spaces = 4
        # body_spaces = 5 - len(body_shown)
        echo("|" + " "*body_spaces + body_shown)
    else:
        echo("|")
    if misses >= 5:
        five_misses = "/"
        six_misses = "/ \\"
        miss_vector_legs = ["","", "", "", five_misses, six_misses]
        legs_shown = miss_vector_legs[misses-1]
        legs_spaces = 3
        echo("|" + " "*legs_spaces + legs_shown)
    else:
        echo("|")

    echo("|")
    echo("|\\")
    echo("| \\")
    echo("|__\\______")

def create_client_msg(msg):
    return ("/").join([str(len(msg)), msg])

def split_server_msg(msg):
    msg = msg.split("/")
    data = msg[3]
    word, incorrect_guesses, is_correct, all_correct = data.split("/")
    return word, list(incorrect_guesses), is_correct, all_correct

if len(sys.argv) > 1:
    port = int(sys.argv[1])
else:
    port = 50000

host = socket.gethostname()
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host, port))

data = client_socket.recv(1024)
isRunning = False
if data == "OK":
    print("Welcome to Hangman!")
    user_input = raw_input("\tENTER ANY KEY TO BEGIN \n\tENTER Q TO QUIT\n$").lower()
    if user_input == "q":
        msg = create_client_msg("q")
        client_socket.send(msg)
        isRunning = False
    else:
        msg = create_client_msg("OK")
        client_socket.send(msg)
        isRunning = True
elif data == 'q' or data == 'Q':
    #Second attempt for error handling
    client_socket.close()
    time.sleep(0.1)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    # client_socket.send(msg)
    msg = client_socket.recv(1024)
    if msg == 'q' or msg == 'Q':
        print("\n*******************************************")
        print("Error: Too Many Clients Already Connected")
        print("Try Again Later")
        print("*******************************************\n")
    # client_socket.send("OK")
        client_socket.close()
        isRunning = False
    else:
        isRunning = True
if isRunning == True:
    msg = client_socket.recv(1024)
    print("msg: %s" % msg)
    # word, incorrect_guesses, _, _ = msg.split("/")
    word, incorrect_guesses, _, _ = split_server_msg(msg)
    # print(word)
    incorrect_guesses = list(incorrect_guesses)
    # print("Incorrect Guesses: %s" % str(incorrect_guesses))
    # isRunning = True
    while isRunning:
        border = "***************************"
        echo(border)
        echo("Incorrect Guesses: %s" % str(", ".join(incorrect_guesses)) )
        num_guesses_left = 6 - len(incorrect_guesses)
        draw_hangman(len(incorrect_guesses))
        echo(border)
        echo("%s Guess(es) Left!" % str(num_guesses_left))
        guess = raw_input("Please Enter a Guess\n\t%s\n$" % str(word)).lower()

        if guess.isalpha() and len(guess) == 1 and guess not in incorrect_guesses:

            msg = create_client_msg(guess.lower())
            client_socket.send(msg)

            msg = client_socket.recv(1024)
            word, incorrect_guesses, is_correct, all_correct = split_server_msg(msg)
            # print("Received Message here: %s" % str(msg))

            # word = msg[0]
            # incorrect_guesses = list(msg[1])
            # is_correct = msg[2]
            # all_correct = msg[3]

            if word == '$INCORRECT$':
                echo(border)
                fail_message = "!You've Lost the Game!"
                echo(fail_message)
                draw_hangman(6)
                # print(fail_message)
                print("")
                echo(border)
                echo('LOSER!!!', 2)
                echo(border + "\n\n")
                isRunning = False
            else:
                # print("Received Message here: %s" % str(msg))

                echo("***************************")
                if is_correct == "True":
                    echo("Great Guess!")
                    if all_correct == "True":
                        echo("Victor!")
                        draw_hangman(len(incorrect_guesses))
                        isRunning = False
                else:
                    echo("Wrong!")

                echo(word)
                echo("Incorrect Guesses: %s" % str((", ").join(incorrect_guesses)))
                echo("***************************\n\n")
        elif guess in incorrect_guesses:
            print("\n")
            echo("Letter Already Guessed!!")
            echo("Please Choose a New Letter!")
        else:
            print("\n")
            echo("WRONG INPUT!")
            echo("Please Write a Single Letter!")



    client_socket.close()
