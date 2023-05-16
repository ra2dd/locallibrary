# Generating Isbn

import random

def getRandomISBN():
    a = 0
    b = 9999999999999

    randomNumber = random.randint(a, b)

    rnLength = len(str(randomNumber))

    if(rnLength < 13):
        zeros = ''
        for x in range(13 - rnLength):
            zeros += '0'
        randomNumber = f'{ zeros }{ str(randomNumber) }'

    # print(randomNumber)
    return randomNumber