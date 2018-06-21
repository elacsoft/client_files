import gender_id_main as gender_lib
import intent as intent_lib
import toxic as toxic_lib
import passion as passion_lib 
from time import sleep
from test2 import passion_new
def genderFunc(name):
    genderVar = gender_lib.main(name)
    return genderVar

def intentFunc(comment, arabic):
    commentVar, argVar = intent_lib.main(comment, arabic)
    return commentVar, argVar

def toxicFunc(comment):
    intentVar = toxic_lib.main(comment)
    return intentVar

def passionFunc():
    t = passion_new()
    return t


#def Main():
#    take1 = input("name: ")
#    take2 = input("comment: ")
#    take3 = input("y or n for arabic: ")
#    print("Working on Gender Code...")
#    sleep(2)
#    print("genderFunc" + str(genderFunc(take1)))
#    print("Working on intent  Code...")
#    sleep(2)
#    print("intentFunc" + str(intentFunc(take2, take3)))
#    print("Working toxic Code...")
#    sleep(2)
#    print("toxicFunc" + str(toxicFunc(take2)))
#    print("Working on passion Code...")
#    sleep(2)
#    t = passion_new()
#    print(t)
#    passionFunc()
#if __name__ == "__main__":
#    Main()

