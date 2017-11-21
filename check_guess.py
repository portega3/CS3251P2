def check_guess(correct_word, current_guesses, guess, initializing=False):
    # return_string = ""
    # correct_guess = False
    # if current == "":
    #     for x in range(len(correct_word)):
    #         return_string = return_string +  "_ "
    # else:
    #     for x in range(len(correct_word)):
    #         if guess == correct_word[x]:
    #             return_string = return_string + correct_word[x] + " "
    #             correct_guess = True
    #         else:
    #             return_string = return_string + current[x] + " "
    # return return_string[:-1], correct_guess, current\
    is_correct = False
    return_string = ""

    # print("guess: %s" % guess)
    if initializing == True:
        for x in range(len(correct_word)):
            return_string = return_string +  "_ "
    else:
        current_guesses.append(guess)
        for letter in list(correct_word):
            if letter in current_guesses:
                return_string = return_string + "{} ".format(letter)
                is_correct = True
            else:
                return_string = return_string + "_ "
    return return_string, current_guesses, is_correct

if __name__ == "__main__":
    correct_word = "jiff"
    return_string, current_guesses, is_correct = check_guess(correct_word, [], [], initializing=True)
    # print("Current: %s" % str(current))
    print(return_string)
    while True:
        guess = raw_input("Enter Guess\n$")
        return_string, correct_guess, is_correct = check_guess(correct_word, current_guesses, guess)
        print(return_string)
