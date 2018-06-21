import subprocess
import time
def passion_new():
    output = subprocess.run("python3 test.py", shell=True, stdout=subprocess.PIPE,universal_newlines=True)
#    time.sleep(2)
#print("................")
    return (output.stdout)


#d = passion_new()
#print(d)
