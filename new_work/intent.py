# initialize lists to store intent words for different languages
french_intents = list()
arabic_intents = list()
arabizi_intents = list()


def get_test_data(filename, arabic=False):
    """
    this function fetches test data from specified file, which conatins 1 comment per line
    :param filename: file to fetch data from
    :return: list of comments
    """

    data = list()
    if not arabic:
        with open(filename, encoding="ISO-8859-1") as inFile:
            for line in inFile:
                data.append(line)
    else:
        with open(filename) as inFile:
            for line in inFile:
                data.append(line.encode().decode('utf8'))


    # clean the data
    data = [x.strip() for x in data]

    # remove repeating elements by creating a set
    data = set(data)
    # convert back to list
    data = list(data)

    return data


def get_data(filename, arabic=False):
    """
    This function fetches list of intent words from the specified file
    :param filename: filename to fetch data from
    :return: list of words
    """

    data = list()
    if not arabic:
        with open('intent_data/' + filename, encoding="ISO-8859-1") as inFile:
            for line in inFile:
                for word in line.split():
                    data.append(word)
    else:
        with open('intent_data/' + filename) as inFile:
            for line in inFile:
                data.append(line.encode().decode('utf8'))

    data = [x.strip() for x in data]

    data = set(data)
    data = list(data)

    # print(data)

    return data


def check_intent(comment, arabic=False):
    """
    Checks intent of a comment (this is the actual logic performing function
    :param comment: a string to test for intent
    :return: INTENT or NO
    """
    global french_intents, arabic_intents, arabizi_intents

    comment = comment.split()

    intent_count = 0

    # these words represent definite intents, so if any of these exists we'll mark the comment has intent directly
    definite_intent = ['خاصك', 'بغيت', 'quelle', 'بغيتكو', 'نصوب', 'سأعطيكم', 'بغيتكم', 'préfère', 'نستعمل', 'تنصحيني', 'خاصني', 'مومكين', 'بغينها', 'بغينا', 'اعطي']

    for c in comment:
        if c in definite_intent:
            intent_count += 4
        if c[-1:] == "?":
            intent_count += 4

        if c in french_intents or c in arabic_intents or c in arabizi_intents:
            intent_count += 1

    # if intent_count >= 4:
    if intent_count >= 2 or (intent_count >= 1 and arabic):
        return "INTENT"
    else:
        return "NO"


def main(comment, arabic):
    global french_intents, arabic_intents, arabizi_intents

    # put all intent file names here, and put the files in data directory
    files = ['french_needs.csv', 'french_wants.csv', 'arabic_intents.csv', 'arabizi_needs.csv', 'arabizi_wants.csv']

    french_intents += get_data(files[0])
    french_intents += get_data(files[1])

    arabic_intents += get_data(files[2], arabic=True)

    arabizi_intents += get_data(files[3])
    arabizi_intents += get_data(files[4])

    # uncomment this line to test the script in terminal with manually entering a comment
    #comment = input("Enter a comment: ")
    # arabic = input("Is this comment in Arabic? (y/n) ").lower()
    arabic = ''
    #while arabic != 'y' and arabic != 'n':
        #arabic = input("Is this comment in Arabic? (y/n) ").lower()
    if arabic == 'y':
        ar = True
    else:
        ar = False

    return (check_intent(comment, ar))

    # put test data file in same directory as this script and give it's name below
    # test_data = list()
    # test_data += get_test_data('french_test.csv')
    # test_data += get_test_data('arabic_test.csv', arabic=True)
    # test_data += get_test_data('arabizi_test.csv')
    #
    # print(test_data)
    #
    # for i, t in enumerate(test_data):
    #     # print(i)
    #     print(check_intent(t, arabic=True) + " : " + t)


#if __name__ == "__main__":
 #   main()
