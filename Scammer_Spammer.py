#Import Libraries
import names, requests, random, string, os, urllib3, threading, time, sys
from multiprocessing import Value
from collections import deque

#for colorful text
class bcolors:
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

http_codes = {
    200: bcolors.GREEN + "200 OK" + bcolors.ENDC,
    403: bcolors.FAIL + "403 FORBIDDEN" + bcolors.ENDC,
    420: bcolors.GREEN + "blaze it everyday" + bcolors.ENDC,
    429: bcolors.FAIL + "429 TOO MANY REQUESTS" + bcolors.ENDC
    }

#Add proxies here. Need both HTTP and HTTPS.
proxies = {}

# Email provider list
email_provider = ['@yahoo.com', '@gmail.com', '@gmx.com', '@icloud.com', '@mail.com', '@gmx.us', '@outlook.com', '@aol.com', '@comcast.net']

#Create the session and set the proxies.
s = requests.Session()
#Uncomment below if you need to use proxies.
#s.proxies = proxies

chars = string.ascii_letters + string.digits + '!@#$%^&*()'
random.seed = (os.urandom(1024))

#Replace with Scammer URL (Usually ends in .PHP but doesn't have to)
url = 'REPLACE WITH URL'

def averageDaemon():
    global count_per_sec
    count_per_sec = 0.0
    oldcount = 0
    average_deque = deque([0],maxlen=25)
    print("AverageDaemon initialized...")
    while True:
        time.sleep(0.2)
        average_deque.append(counter.value - oldcount)
        count_per_sec = (sum(average_deque) / len(average_deque)) * 5
        oldcount = counter.value


def sendRequests():
    global counter
    global count_per_sec
    running = True
    
    print('Thread ' + bcolors.YELLOW + str(threads.value) + bcolors.ENDC + ' started')
    while running:
        #Generate random first/last name
        first = names.get_first_name().lower()
        last = names.get_last_name().lower()
    
        #Generate 3 random numbers
        rando = ''.join(random.choice(string.digits))
        rando2 = ''.join(random.choice(string.digits))
        rando3 = ''.join(random.choice(string.digits))

        #Chooses email format
        emailformat = random.choice([1,2,3,4,5,6,7,8,9,10,11])
        if emailformat == 1:        
            name = first + last + rando + rando2 + rando3
        if emailformat == 2:
            name = first + '_' + last + rando + rando2 + rando3
        if emailformat == 3:
            name = first + '-' + last + rando + rando2
        if emailformat == 4:
            name = last + first + rando + rando2 + rando3
        if emailformat == 5:
            name = first + rando + rando2 + last
        if emailformat == 6:
            name = last + rando + rando2 + rando3 + first
        if emailformat == 7:
            name = last + '-' + first + '-' + rando + rando2 + rando3 
        if emailformat == 8:
            name = first + last
        if emailformat == 9:
            name = last + first
        if emailformat == 10:
            name = first + rando + rando2 + rando3
        if emailformat == 11:
            name = first + '_' + last

        username = name.lower() + random.choice(email_provider)

        #Chooses randomly generated password between 8-16 characters long
        password = ''.join(random.choice(chars) for i in range(random.choice([8,8,8,9,10,11,12,13,14,15,16,17,18,19,20])))

        #Disables HTTPS warning
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        #Make post request
        #Replace parameters as needed.
        req=s.post(url, allow_redirects=False, verify=False, data={
            'login': username,
            'password': password
        })
        
        #increment the counter on successful request
        if req.ok:
            with counter.get_lock():
                counter.value += 1

        #Print Info
        print()
        print(bcolors.CYAN + "Sending username: " + bcolors.YELLOW + username + bcolors.CYAN + " and Password: " + bcolors.YELLOW + password + bcolors.CYAN)
        print("To: " + req.url)
        print(bcolors.YELLOW + str(counter.value) + bcolors.FAIL + " requests sent, " + bcolors.YELLOW + str('%.2f' % count_per_sec) + bcolors.FAIL + " req/second, " + bcolors.YELLOW + str(threads.value) + bcolors.FAIL + " threads active" + bcolors.ENDC)
        
        return_code = http_codes.get(req.status_code, bcolors.YELLOW + str(req.status_code) + bcolors.ENDC)
        print(bcolors.BLUE + "STATUS: " + return_code + bcolors.ENDC)

        time.sleep(1)
        with stopflag.get_lock():
            #if stopflag is 1, one thread will recognize this and terminate
            if stopflag.value == 1:
                running = False
                stopflag.value = 0
                with threads.get_lock():
                    #thread safe decrement for threads counter
                    threads.value -= 1

if __name__ == '__main__':
    start_time = time.time()
    print("#####################################")
    print("##########                 ##########")
    print("##########    Quad_Plex'   ##########")
    print("########## Scammer Spammer ##########")
    print("##########                 ##########")
    print("#####################################")
    print()
    print("Usage Instructions:")
    print("    type '+' and press Enter to add threads")
    print("    type '-' and press Enter to remove threads")
    print("    when the threadcount reaches 0, the script stops automatically")
    print()
    print("SCREW SCAMMERS!!!!")
    print()

    global counter
    counter = Value('i', 1)

    global stopflag
    stopflag = Value('i', 0)
    
    global threads
    threads = Value('i', 0)

    global count_per_sec
    
    average_daemon = threading.Thread(target=averageDaemon, args=(), kwargs={}, daemon=True)
    average_daemon.start()

    while True:
        action = input()
        if action == "+":
            #spawn a new thread and increase counter
            thr = threading.Thread(target=sendRequests, args=(), kwargs={})
            with threads.get_lock():
                threads.value += 1
            thr.start()
        elif action == "-":
            #set the stopflag to 1, the first thread to grab this lock Value will exit and set it back to 0
            with stopflag.get_lock():
                stopflag.value = 1
        time.sleep(0.5)
        #exit if all threads are stopped
        with threads.get_lock():
            if threads.value == 0:
                print()
                sys.exit(str(counter.value) + " requests sent over a period of " + str((time.time() - start_time)) + " seconds")

