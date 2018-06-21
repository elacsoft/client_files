men_prefixes = list()
women_prefixes = list()
men_names = list()
women_names = list()


def get_data(language, detail, arabic=False):
    """
    This function fetches list of intent words from the specified file
    :param language: filename to fetch data from
    :param detail:
    :param arabic:
    :return: list of words
    """

    data = list()
    path = 'gender_data/' + language + '/'

    if detail[0] == 'm':
        path += 'men'
    else:
        path += 'women'

    if detail[1] == 'p':
        path += '/prefixes.csv'
    else:
        path += '/names.csv'

    if not arabic:
        with open(path, encoding='ISO-8859-1') as inFile:
            for line in inFile:
                data.append(line)
    else:
        with open(path) as inFile:
            for line in inFile:
                data.append(line.encode().decode('utf8'))

    data = [x.strip() for x in data]

    data = set(data)
    data = list(data)

    print(data)

    return data


def check_gender(name):
    if any(prefix in name for prefix in men_prefixes) or any(prefix in name for prefix in men_names):
        return "Male"

    if any(prefix in name for prefix in women_prefixes) or any(prefix in name for prefix in women_names):
        return "Female"

    return "Not Sure!"


def main(name):
    global men_prefixes, men_names, women_prefixes, women_names

    languages = ['english']
    for language in languages:
        is_arabic = False
        if language == 'arabic':
            is_arabic = True

        men_prefixes += get_data(language, 'mp', is_arabic)
        men_names += get_data(language, 'mn', is_arabic)
        women_prefixes += get_data(language, 'wp', is_arabic)
        women_names += get_data(language, 'wn', is_arabic)

    #name = input("Enter a name >>> ")
    return (check_gender(name))


#if __name__ == "__main__":
#    main()
