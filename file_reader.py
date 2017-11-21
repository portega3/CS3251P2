def open_file(filename):
    words = []
    with open(filename, 'r') as fh:
        for line in fh:
            words.append(line.rstrip('\n'))

    words = words[1:]
    
    print(str(words))

if __name__ == "__main__":
    open_file("words.txt")
