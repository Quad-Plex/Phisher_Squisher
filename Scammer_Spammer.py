#Import Libraries
import names, requests, random, string, os, urllib3, threading, time
from multiprocessing import Value

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

def sendRequests():
    global counter
    running = True

    print('Thread ' + bcolors.YELLOW + str(threads) + bcolors.ENDC + ' started')
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
                    'password': password,
        })
        
        #Print Info
        print()
        print(bcolors.CYAN + "Sending username: " + bcolors.YELLOW + username + bcolors.CYAN + " and Password: " + bcolors.YELLOW + password + bcolors.CYAN)
        print("To: " + req.url)
        print(bcolors.YELLOW + str(counter.value) + bcolors.FAIL + " times with " + bcolors.YELLOW + str(threads) + bcolors.FAIL + " threads" + bcolors.ENDC)
    
        if req.ok:
            with counter.get_lock():
                counter.value += 1
            print(bcolors.BLUE + "STATUS: " + bcolors.GREEN + str(req.status_code) + bcolors.ENDC)
        else:
            print(bcolors.BLUE + "STATUS: " + bcolors.FAIL + str(req.status_code) + bcolors.ENDC)

        with stopflag.get_lock():
            if stopflag.value == 1:
                running = False
                stopflag.value = 0
        time.sleep(1)

if __name__ == '__main__':
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

    global counter
    counter = Value ('i', 1)

    global stopflag
    stopflag = Value ('i', 0)
    
    global threads
    threads = 0

    while True:
        action = input()
        if action == "+":
            #spawn a new thread and increase counter
            thr = threading.Thread(target=sendRequests, args=(), kwargs={})
            threads += 1
            thr.start()
        elif action == "-":
            #set the stopflag to 1, the first thread to grab this lock Value will exit and set it back to 0
            with stopflag.get_lock():
                stopflag.value = 1
            threads -= 1

        #exit if all threads are stopped
        if threads == 0:
            break
            
