# initialize lists to store intent words for different languages
french_entities = list()
arabic_entities = list()
arabizi_entities = list()


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
        with open('toxic_data/' + filename, encoding="ISO-8859-1") as inFile:
            for line in inFile:
                # for word in line.split():
                data.append(line)
    else:
        with open('toxic_data/' + filename) as inFile:
            for line in inFile:
                data.append(line.encode().decode('utf8'))

    data = [x.strip() for x in data]

    data = set(data)
    data = list(data)

    # print(data)

    return data


def check_intent(comment):
    """
    Checks intent of a comment (this is the actual logic performing function
    :param comment: a string to test for intent
    :return: INTENT or NO
    """
    global french_entities, arabic_entities, arabizi_entities

    for fe in french_entities:
        if fe in comment:
            return "Toxic"

    for fe in arabic_entities:
        if fe in comment:
            return "Toxic"

    for fe in arabizi_entities:
        if fe in comment:
            return "Toxic"

    return "Not Toxic"


def main(comment):
    global french_entities, arabic_entities, arabizi_entities

    # put all intent file names here, and put the files in data directory
    files = ['toxic_arabic.csv', 'toxic_arabizi.csv']

    arabic_entities += get_data(files[0], arabic=True)

    arabizi_entities += get_data(files[1])

    # uncomment this line to test the script in terminal with manually entering a comment
    #comment = input("Enter a comment: ")
    return (check_intent(comment))

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
