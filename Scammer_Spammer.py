# Import Libraries
from collections import deque
from multiprocessing import Value
from pynput import keyboard

import names
import os
import random
import requests
import string
import sys
import threading
import time
import urllib3


# for colorful text
class Colors:
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


http_codes = {
    200: Colors.GREEN + "200 OK" + Colors.ENDC,
    302: Colors.GREEN + "302 FOUND" + Colors.ENDC,
    403: Colors.FAIL + "403 FORBIDDEN" + Colors.ENDC,
    404: Colors.FAIL + "404 NOT FOUND" + Colors.ENDC,
    420: Colors.GREEN + "420 blaze it everyday" + Colors.ENDC,
    429: Colors.FAIL + "429 TOO MANY REQUESTS" + Colors.ENDC,
    500: Colors.FAIL + "500 INTERNAL SERVER ERROR" + Colors.ENDC,
    503: Colors.FAIL + "503 SERVICE UNAVAILABLE GET FUCKED!!" + Colors.ENDC
}

# Email provider list
email_provider = ['@yahoo.com', '@gmail.com', '@gmx.com', '@icloud.com', '@mail.com', '@gmx.us', '@outlook.com',
                  '@aol.com', '@comcast.net', '@fuckyou.com', '@screwscammers.com', '@cocksucker.com', '@no.com',
                  '@nicetry.com']

# Create the session and set the proxies.
s = requests.Session()
# Uncomment below if you need to use proxies.
# s.proxies = proxies

chars = string.ascii_letters + string.digits + '!@#$%^&*()'
random.seed = (os.urandom(1024))

global threads
threads = []

# Replace with Scammer URL (Usually ends in .PHP but doesn't have to)
url = 'REPLACE WITH URL'

# Add headers as "key": "value" pairs
# The user-agent is a basic example and seems to work well
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/113.0.0.0 Safari/537.36 OPR/99.0.0.0 (Edition std-1)"
}

# Add cookies as "key": "value" pairs
cookies = {}

# Add proxies here. Need both HTTP and HTTPS.
proxies = {}


def backgroundaemon():
    global count_per_sec
    count_per_sec = 0.0
    oldcount = 0
    average_deque = deque([0], maxlen=25)
    print("BackgroundDaemon initialized...")
    while True:
        # thread-table cleanup
        for thread in threads:
            if not thread.is_alive():
                thread.join()
                threads.remove(thread)
        # calculate the average num of requests
        average_deque.append(counter.value - oldcount)
        count_per_sec = (sum(average_deque) / len(average_deque)) * 5
        oldcount = counter.value
        time.sleep(0.2)


def sendrequests():
    global counter
    global count_per_sec
    running = True

    print('Thread ' + Colors.YELLOW + str(len(threads)) + Colors.ENDC + ' started')
    while running:
        # Generate random first/last name
        first = names.get_first_name().lower()
        last = names.get_last_name().lower()

        # Generate 3 random numbers
        rando = ''.join(random.choice(string.digits))
        rando2 = ''.join(random.choice(string.digits))
        rando3 = ''.join(random.choice(string.digits))

        # Chooses email format
        emailformat = random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])
        generated_username = ""
        if emailformat == 1:
            generated_username = first + last + rando + rando2 + rando3
        if emailformat == 2:
            generated_username = first + '_' + last + rando + rando2 + rando3
        if emailformat == 3:
            generated_username = first + '-' + last + rando + rando2
        if emailformat == 4:
            generated_username = last + first + rando + rando2 + rando3
        if emailformat == 5:
            generated_username = first + rando + rando2 + last
        if emailformat == 6:
            generated_username = last + rando + rando2 + rando3 + first
        if emailformat == 7:
            generated_username = last + '-' + first + '-' + rando + rando2 + rando3
        if emailformat == 8:
            generated_username = first + last
        if emailformat == 9:
            generated_username = last + first
        if emailformat == 10:
            generated_username = first + rando + rando2 + rando3
        if emailformat == 11:
            generated_username = first + '_' + last

        generated_email = generated_username.lower() + random.choice(email_provider)

        # Chooses randomly generated password between 8-16 characters long
        password = ''.join(random.choice(chars) for i in
                           range(random.choice([8, 8, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20])))

        # The actual POST form payload data
        payload = {
            'login': generated_email,
            'password': password,
        }

        # Disables HTTPS warning
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        # Make post request
        # Replace parameters as needed.
        req = s.post(url, allow_redirects=False, verify=False, headers=headers, cookies=cookies, data=payload)

        # increment the counter on successful request
        if req.ok:
            with counter.get_lock():
                counter.value += 1

        # Print Info
        print()
        print(
            Colors.CYAN + "Sending username: " + Colors.YELLOW + generated_email +
            Colors.CYAN + "and password: " + Colors.YELLOW + password + Colors.CYAN)
        print("To: " + req.url)
        print(Colors.YELLOW + str(counter.value) + Colors.FAIL + " requests sent, " + Colors.YELLOW +
              str('%.1f' % count_per_sec) + Colors.FAIL + " req/second, " + Colors.YELLOW + str(len(threads)) +
              Colors.FAIL + " threads active" + Colors.ENDC)

        return_code = http_codes.get(req.status_code, Colors.YELLOW + str(req.status_code) + Colors.ENDC)
        print(Colors.BLUE + "STATUS: " + return_code + Colors.ENDC)

        if req.status_code == 403 or req.status_code == 429 or req.status_code == 503:
            print("Careful there cowboy, removing a thread...")
            running = False

        time.sleep(1)

        with stopAllFlag.get_lock():
            if stopAllFlag.value == 1:
                running = False

        with stopFlag.get_lock():
            # if stopflag is 1, one thread will recognize this and terminate
            if stopFlag.value == 1:
                running = False
                stopFlag.value = 0


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
    print("    press '+' to add threads")
    print("    press '-' to remove threads")
    print("    press '*' to remove ALL threads")
    print("    press '/' to terminate")
    print()
    print("SCREW SCAMMERS!!!!")
    print()

    global counter
    counter = Value('i', 0)

    global stopFlag
    stopFlag = Value('i', 0)

    global stopAllFlag
    stopAllFlag = Value('i', 0)

    global count_per_sec

    background_daemon = threading.Thread(target=backgroundaemon, args=(), kwargs={}, daemon=True)
    background_daemon.start()

    while True:
        with keyboard.Events() as events:
            # Block for as much as possible
            event = events.get(1e6)
            if event.key == keyboard.KeyCode.from_char("+"):
                # spawn a new thread and increase counter
                thr = threading.Thread(target=sendrequests, args=(), kwargs={})
                threads.append(thr)
                thr.start()
            elif event.key == keyboard.KeyCode.from_char("-"):
                # set the stopflag to 1, the first thread to grab this lock Value will exit and set it back to 0
                with stopFlag.get_lock():
                    stopFlag.value = 1
            elif event.key == keyboard.KeyCode.from_char("*"):
                print("!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                print("!!Stopping all threads...!!")
                print("!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                stopAllFlag.value = 1
            elif event.key == keyboard.KeyCode.from_char("/"):
                print()
                sys.exit(str(counter.value) + " requests sent over a period of " + str(
                    (time.time() - start_time)) + " seconds")
            time.sleep(0.1)
