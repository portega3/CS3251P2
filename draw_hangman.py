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
        six_misses = " / \\"
        miss_vector_legs = ["","", "", "", five_misses, six_misses]
        legs_shown = miss_vector_legs[misses-1]
        legs_spaces = 2
        echo("|" + " "*legs_spaces + legs_shown)
    else:
        echo("|")

    echo("|")
    echo("|\\")
    echo("| \\")
    echo("|__\\______")


if __name__ == "__main__":
    misses = int(sys.argv[1])
    draw_hangman(misses)
