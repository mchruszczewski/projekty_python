word= 'polska'


def hangman (word):
    """Outcome of this function is popular hangman game"""
    print("Let's play hangman!")
    chances= 12
    word= list(word)
    user_word =[]
    [user_word.append('_')for i in range (0,len(word))]
    while chances>0 and user_word != word:
            guess= input("Please guess a letter: ")
            if guess in word:
                print('That is correct!')
                for i in range (0,len(word)):
                    if word[i] == guess:
                        user_word[i]=guess
                print (f"So far, so good! You guess a letter and you have {chances} left. You have so far guess these letters {user_word}") if user_word != word else print ("Congratulations!")
            else:
                print('That is not correct!')
                chances -= 1
                print (f"You have {chances} left. Please try again!") if 0<chances else print("Sorry!")
    print("You won!") if user_word==word else print("You lost!")

hangman(word)


word= 'polska'


def hangman (word):
    """Outcome of this function is popular hangman game"""
    print("Let's play hangman!")
    chances= 12
    word= list(word)
    user_word =[]
    [user_word.append('_')for i in range (0,len(word))]
    while chances>0 and user_word != word:
            guess= input("Please guess a letter: ")
            if guess in word:
                print('That is correct!')
                for i in range (0,len(word)):
                    if word[i] == guess:
                        user_word[i]=guess
                print (f"So far, so good! You guess a letter and you have {chances} left. You have so far guess these letters {user_word}") if user_word != word else print ("Congratulations!")
            else:
                print('That is not correct!')
                chances -= 1
                print (f"You have {chances} left. Please try again!") if 0<chances else print("Sorry!")
    print("You won!") if user_word==word else print("You lost!")

hangman(word)