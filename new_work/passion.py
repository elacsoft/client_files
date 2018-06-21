import re
import time
import pyodbc
# initialize lists to store intent words for different languages
arabic_passion_entities = list()
french_passion_entities = list()
arabizi_passion_entities = list()


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
        with open('data2/' + filename, encoding="ISO-8859-1") as inFile:
            for line in inFile:
                for word in line.split():
                    data.append(word)
    else:
        with open('data2/' + filename) as inFile:
            for line in inFile:
                data.append(line.encode().decode('utf8'))

    data = [x.strip() for x in data]

    data = set(data)
    data = list(data)

    # print(data)

    return data


def check_passion(comment, arabic=False):
    """
    Checks intent of a comment (this is the actual logic performing function
    :param comment: a string to test for intent
    :return: INTENT or NO
    """
    global french_passion_entities, arabic_passion_entities, arabizi_passion_entities
    comment = comment.split()

    passion_count = 0

    # these words represent definite intents, so if any of these exists we'll
    # mark the comment has intent directly
    definite_passion = ['Bravos', 'Bravo', 'Bravooo' 'Zwina', 'belle', 'top', 'Ahsan',  'A7san', 'A7ssen' 'A3jabani', '3jebni', 'Ahsen', 'toppppp', 'super', 'genial', 'magnifique', 'bien', 'Good', 'Best', 'واوووووووو','جميلة', 'ماعمري انبدلهم', 'ياااااسلام', 'يد مبارك سعيد', 'مبروك عليكم', 'روعه', 'اعمرها']
    for c in comment:
        # Replace multiple dots with space
        line = re.sub('\.\.+', ' ', c)
        # Remove single dots
        c = re.sub('\.', '', line)

        if c in definite_passion:
            passion_count += 4
        if c[-1:] == "?":
            passion_count += 4

        if c in french_passion_entities or c + "e" in french_passion_entities or c in arabic_passion_entities or c in arabizi_passion_entities:
            passion_count += 1

        if c in ['Bravo', 'Bravoo', 'Bravooo', 'Bravoooo', 'Bravooooo', 'BRAVO']:
            passion_count += 3


        if c in arabic_passion_entities:
            passion_count += 2

        if c in arabizi_passion_entities:
            passion_count += 4

        if c in ['brit', 'Brit']:
            passion_count -= 20


    # if intent_count >= 4:
    if passion_count > 2 or (passion_count >= 2 and arabic):
        return "PASSION"
    else:
        return "NO"


def main():
    global french_passion_entities, arabic_passion_entities, arabizi_passion_entities

    # put all intent file names here, and put the files in data directory
    files = ['french_passions.csv', 'arabic_passions.csv', 'arabizi_passions.csv']

    french_passion_entities += get_data(files[0])
    #
    arabic_passion_entities += get_data(files[1], arabic=True)
    #
    arabizi_passion_entities += get_data(files[2])

    # uncomment this line to test the script in terminal with manually entering
    # a comment
    # comment = input("Enter a comment: ")
    # arabic = input("Is this comment in Arabic?  (y/n ").lower()
    # while arabic != 'y' or arabic != 'n':
    #     arabic = input("Is this comment in Arabic?  (y/n ").lower()
    #     if arabic == 'y':
    #         ar = True
    #     else:
    #         ar = False

   # print(check_passion(comment))

    # put test data file in same directory as this script and give it's name
    # below
    test_data = list()
    test_data += get_test_data('french_test.csv')
    # test_data += get_test_data('arabic_test.csv', arabic=True)
    # test_data += get_test_data('arabizi_test.csv')
    #
    # print(test_data)
    #
    for i, t in enumerate(test_data):
        #print(i)
        print(check_passion(t, arabic=False) + " : " + t)
    



    generate_backup(test_data) # generate backup of entities
    prev_passion_index = dict()
    prev_passions = dict()
    while(True):
        # brands and sectors
        brands = ["Orangina Maroc",""] # these two lists must be of same length
        sectors = ["","Sports Club"]
        total_like_ratio_brand = 0
        total_like_ratio_sector =0

        total_engagement_ratio_brand = 0
        total_engagement_ratio_sector =0
        is_sector = False
        for i in range(len(brands)):
            name = brands[i]
            if name == "":
                is_sector = True
                name = sectors[i]
            print("------------------------")
            print(name)
            (passionIndex,likeRatio,engagementRatio) = get_passion_index(test_data,sectors[i],brands[i]) #provide data here
            if is_sector:
                total_like_ratio_sector += likeRatio
                total_engagement_ratio_sector += engagementRatio
            else:
                total_like_ratio_brand += likeRatio
                total_engagement_ratio_brand += engagementRatio

            prevPasInd = 0
            if name in prev_passion_index.keys():
                prevPasInd = prev_passion_index[name]
            print("Net Chnage : " + str((passionIndex - prevPasInd)))
            prev_passion_index[name] = passionIndex

            if name in prev_passions.keys():
                prev_passions[name] = prev_passions[name].append(passionIndex)
            else:
                prev_passions[name] = [passionIndex]

        print("")
        print("Average ratio of likes per brand : "+str((total_like_ratio_brand / len(brands))))
        print("Average ratio of likes per sector : "+str((total_like_ratio_sector / len(brands))))

        print("Average ratio of engagement per brand : "+str((total_engagement_ratio_brand / len(brands))))
        print("Average ratio of engagement per sector : "+str((total_engagement_ratio_sector / len(brands))))
        time.sleep(14440)




def generate_backup(entity_list):
    try:
        cnxn = pyodbc.connect(r'DRIVER={ODBC Driver 13 for SQL Server};'
        r'SERVER=DESKTOP-ALLGF1Q\SQLSERVEREXPRESS;'
        r'DATABASE=ScrapyWeb;'
        r'UID=sa;'
        r'PWD=facon')
    except Exception as e:
        print(e)
    cursor = cnxn.cursor()
    for w in entity_list:
        query = "insert into backup_entity_list(words) values ('"+w.replace("'","")+"')"
        cursor.execute(query)
    cnxn.commit()
    cnxn.close()
    


def get_passion_index(entity_list,sector,brand):
    try:
        cnxn = pyodbc.connect(r'DRIVER={ODBC Driver 13 for SQL Server};'
        r'SERVER=DESKTOP-ALLGF1Q\SQLSERVEREXPRESS;'
        r'DATABASE=ScrapyWeb;'
        r'UID=sa;'
        r'PWD=facon')
    except Exception as e:
        print(e)
    cursor = cnxn.cursor()
    query = ""
    if brand != "":
        query = "select sum(p.likes_count), sum(p.comments_count), sum(p.sharedposts_count) , max(i.fan_count)  from T_FB_POST p right JOIN [dbo].[T_FB_INFLUENCER] i ON i.id = p.fk_influencer  where i.name= '" + brand + "'group by i.name"
    elif sector != "":
        query = "select sum(p.likes_count), sum(p.comments_count), sum(p.sharedposts_count) , max(i.fan_count)  from T_FB_POST p right JOIN [dbo].[T_FB_INFLUENCER] i ON i.id = p.fk_influencer  where i.category= '" + sector + "'group by i.category"
    cursor.execute(query)
    likes_count = 0
    comments_count = 0
    shared_count = 0
    fan_count = 0
    for row in cursor.fetchall():
        likes_count = int(row[0])
        comments_count = int(row[1])
        shared_count = int(row[2])
        fan_count = int(row[3])

    intensityIndex = intensity_index(entity_list ,fan_count)
    print("Intestity Index : " + str(intensityIndex))

    print("Mentions per category : " + str(mentions_per_category(entity_list)))

    engagementRatio = engagement_ratio(shared_count,comments_count,fan_count)
    likeRatio = like_ratio(likes_count,fan_count)
    engagementIndex = engagement_index(engagementRatio,likeRatio)
    print("Engagement Index : " + str(engagementIndex))

    netsentimentIndex = net_sentiment_index(2000,300,500)
    print("Net Sentiment Index : " + str(netsentimentIndex))

    passionIndex = passion_intensity_index(intensityIndex,engagementIndex,netsentimentIndex)
    print("Passion Index : " + str(passionIndex))
    
    return (passionIndex,likeRatio,engagementRatio)



def intensity_index(list_entities,fan_count):
    if fan_count == 0:
        return 0
    return (len(list_entities) / fan_count) * 100


def mentions_per_category(list_entities):
    return len(list_entities)

def engagement_ratio(numOfShares,numOfComments,fan_count):
    if fan_count == 0:
        return 0
    return ((numOfShares + numOfComments) / fan_count) * 100

def like_ratio(likes_count,fan_count):
    if fan_count == 0:
        return 0
    return likes_count / fan_count

def engagement_index(engagement_ratio,like_ratio):
    return int(round((engagement_ratio + like_ratio) / 2,0))

def net_sentiment_index(positve,negative,neutral):
    if (positve + negative + neutral) == 0:
        return 0
    return ((positve - negative) / float(positve + negative + neutral)) * 100

def passion_intensity_index(intensityIndex,engagementIndex,netSentimentIndex):
    return round((intensityIndex + engagementIndex + netSentimentIndex) / float(3),2)








#if __name__ == "__main__":
#    main()
